import re
import json
import tweepy
from datetime import datetime
from nltk.tokenize.casual import TweetTokenizer

client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAACh0VAEAAAAAW7%2BbhWLfUi6hbWgDPP4slRjDk%2FU%3DcCVxvampJjvIVYNFyLlcMG9BBRvbtXf8BzyzDu6dLXmlg2xPbR')

query = '("elections" OR "voter" OR "voté" OR "vote") -is:retweet -is:reply -is:quote lang:fr'
q_macron = 'macron -marine -"le pen" -is:retweet -is:reply -is:quote lang:fr'
q_lepen = '"le pen" -macron -emmanuel -is:retweet -is:reply -is:quote lang:fr'
start = datetime(2022,4,22,23,59)


def fetch_prediction():
    pred_user_log = json.load(open('data/prediction_log.json'))
    prediction = json.load(open('data/prediction.json'))
    load = tweepy.Paginator(client.search_recent_tweets, query=q_macron, tweet_fields=['created_at', 'author_id'], max_results=100, end_time=start).flatten(limit=1000)
    for tweet in load:
        if (not tweet.author_id in pred_user_log['users']) and (not tweet.id in pred_user_log['log']):
            prediction['macron'][str(tweet.id)] = clean_tweet(tweet.text)
            pred_user_log['log'].append(tweet.id)
            pred_user_log['users'].append(tweet.author_id)

    load = tweepy.Paginator(client.search_recent_tweets, query=q_lepen, tweet_fields=['created_at', 'author_id'], max_results=100, end_time=start).flatten(limit=1000)
    for tweet in load:
        if (not tweet.author_id in pred_user_log['users']) and (not tweet.id in pred_user_log['log']):
            prediction['le_pen'][str(tweet.id)] = clean_tweet(tweet.text)
            pred_user_log['log'].append(tweet.id)
            pred_user_log['users'].append(tweet.author_id)
    json.dump(pred_user_log, open("data/prediction_log.json", "w"), indent = 4)
    json.dump(prediction, open("data/prediction.json", "w"), indent = 4)


def fetch_training():
    log = json.load(open('data/training_log.json'))
    npro = json.load(open('data/non_processed.json'))
    last = 0
    if log['last_id'] == "":
        load = tweepy.Paginator(client.search_recent_tweets, query=query, tweet_fields=['context_annotations', 'author_id'], max_results=100).flatten(limit=1000)
    else:
        load = tweepy.Paginator(client.search_recent_tweets, query=query, tweet_fields=['context_annotations', 'author_id'], max_results=100, until_id=log['last_id']).flatten(limit=1000)
    for tweet in load:
        if (not tweet.author_id in log['users']) and (not tweet.id in log['log']):
            npro[str(tweet.id)] = tweet.text
            log['log'].append(str(tweet.id))
            log['users'].append(tweet.author_id)
            last = tweet.id
    log['last_id'] = str(last)
    json.dump(log, open("data/training_log.json", "w"), indent = 4)
    json.dump(npro, open("data/non_processed.json", "w"), indent = 4)


def clean_tweet(tweet):
    t = TweetTokenizer()
    stopwords = json.load(open("data/stopwords.json"))["words"]
    temp = tweet.lower()
    temp = re.sub("@[A-Za-z0-9]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r"([a-z])['’]", r"\1e ", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub(r'&[a-zA-Z]+;', '', temp)
    temp = re.sub(r'[()#@:’,…&«»]', '', temp)
    temp = re.sub(r'[0-9]', '', temp)
    temp = temp.replace('/', '')
    temp = temp.replace('\\', '')
    temp = temp.replace('.', '')
    temp = temp.replace('*', '')
    temp = temp.replace('\"', '')
    temp = temp.replace('\'', '')
    temp = t.tokenize(temp)
    temp = [w for w in temp if not w in stopwords]
    temp = " ".join(word for word in temp)
    return temp