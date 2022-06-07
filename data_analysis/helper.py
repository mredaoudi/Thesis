import csv
import re
import string
import json
import random
from nltk.tokenize.casual import TweetTokenizer


def preprocess(tweet_text):
    tk = TweetTokenizer()
    text = tweet_text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub("@[A-Za-z0-9]+","", text)
    text = re.sub("#[A-Za-z0-9_éàèê]+","", text)
    text = re.sub(r"([a-z])['’]", r"\1e ", text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[«»€$]', '', text)
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    text = text.translate(translator)
    text = " ".join(text.split())
    stopwords = json.load(open('../data/json/stopwords.json'))['words']
    tokens = tk.tokenize(text)
    result = ' '.join([w for w in tokens if w not in stopwords])
    return result


def from_json_to_csv(dataset_name, is_labeled = True):
    dataset = json.load(open('../data/json/' + dataset_name + '.json'))
    header = ['text', 'label'] if is_labeled else ['text']
    with open('../data/csv/' + dataset_name + '.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for tweet, details in dataset.items():
            if details['tweet_data']:
                text = preprocess(details['tweet_data']['text'])
            else:
                text = preprocess(details['previous_processed_text'])
            if is_labeled:    
                writer.writerow([text, details['sentiment_label']])
            else:
                writer.writerow([text])


def lepen_remover():
    lepen = json.load(open('../data/json/prediction_lepen.json'))
    print(len(lepen))
    return

lepen_remover()

def split_training_test():
    preelection = json.load(open('../data/json/pre_election.json'))
    pos = []
    neg = []
    neu = []
    for tweet in preelection:
        if preelection[tweet]['sentiment_label'] == "neu":
            neu.append(tweet)
        elif preelection[tweet]['sentiment_label'] == "pos":
            pos.append(tweet)
        else:
            neg.append(tweet)
    pp = int(len(pos) * 0.20)
    nn = int(len(neg) * 0.20)
    ee = int(len(neu) * 0.20)
    
    pos_rand = random.sample(pos, pp)
    neg_rand = random.sample(neg, nn)
    neu_rand = random.sample(neu, ee)
    
    training = preelection.copy()
    test = {}
    for i in range(ee):
        if i < pp:
            test[pos_rand[i]] = preelection[pos_rand[i]]
            del training[pos_rand[i]]
        if i < nn:
            test[neg_rand[i]] = preelection[neg_rand[i]]
            del training[neg_rand[i]]
        test[neu_rand[i]] = preelection[neu_rand[i]]
        del training[neu_rand[i]]
    
    json.dump(training, open('../data/json/training.json', 'w'), indent=4)
    json.dump(test, open('../data/json/test.json', 'w'), indent=4)
    return


def reload_preprocess():
    from_json_to_csv('training')
    from_json_to_csv('test')
    from_json_to_csv('prediction_macron', False)
    from_json_to_csv('prediction_lepen', False)