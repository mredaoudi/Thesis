import json
import math
import fetcher
from flask import Flask, render_template, request, redirect


app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    npro  = json.load(open("data/non_processed.json"))
    pro = json.load(open("data/processed.json"))
    tot = json.load(open("data/training_log.json"))
    labels = {'pos': 0, 'neg': 0, 'neu': 0}
    
    nkeys = len(npro.keys())
    pkeys = len(pro.keys())
    total = len(tot['log'])
    deleted = total - pkeys - nkeys

    ratio = str(pkeys+deleted) + " out of " + str(total) + " tweets processed"
    progress = 0
    if pkeys != 0:
        progress = int(((pkeys+deleted) / total) * 100)
        for key in pro:
            labels[pro[key][1]] += 1
    return render_template('home.html', progress=progress, ratio=ratio, labels=labels, unprocessed=nkeys, deleted=deleted)


@app.route("/trainer", methods=['GET'])
def trainer():
    return render_template('trainer.html')


@app.route("/fetch", methods=['POST'])
def fetch():
    fetcher.fetch_training()
    fetcher.fetch_prediction()
    return redirect('/')


@app.route("/list", methods=['GET'])
@app.route("/list/<page>", methods=['GET'])
def tlist(page="1"):
    if not page.isnumeric():
        return redirect('/list')
    page = int(page)
    pro = json.load(open("data/processed.json"))
    keys = list(pro.keys())
    if len(keys) == 0:
        return render_template('list.html')
    if page > math.ceil(len(keys)/10):
        page = math.ceil(len(keys) / 10)
        return redirect('/list/' + str(page))
    rang = ((page - 1) * 10, min(page * 10, len(keys)))
    mx = math.ceil(len(keys) / 10)
    load = []
    for i in range(rang[0], rang[1]):
        load.append(pro[keys[i]])
    return render_template('list.html', load=load, page=page, mx=mx)


@app.route("/tweet", methods=['POST', 'GET'])
def tweet():
    npro  = json.load(open("data/non_processed.json"))
    pro = json.load(open("data/processed.json"))
    if request.method == 'POST':
        id = request.json['id']
        label = request.json['label']
        text = request.json['text']
        if label != 'delete':
            pro[id] = [fetcher.clean_tweet(text), label]
        del npro[id]
        json.dump(pro, open("data/processed.json", "w"), indent = 4)
        json.dump(npro, open("data/non_processed.json", "w"), indent = 4)
        return {"success": True}
    
    if npro:
        keys = list(npro.keys())
        number = len(pro.keys()) + 1
        return {
            "empty": False,
            "load": [keys[0], npro[keys[0]], str(number)]
        }
    return {
        "empty": True
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0')
