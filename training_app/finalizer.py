import csv
import re
import string
import json
import random
from nltk.tokenize.casual import TweetTokenizer



def preprocess_tweet(tweet_text):
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


def json_csv(dataset_name):
	dataset = json.load(open('../data/json/' + dataset_name + '.json'))
	header = ['text', 'label']
	with open('../data/csv/' + dataset_name + '.csv', 'w', encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		for tweet, details in dataset.items():
			if details['tweet_data']:
				text = preprocess_tweet(details['tweet_data']['text'])
			else:
				text = preprocess_tweet(details['previous_processed_text'])
			writer.writerow([text, details['sentiment_label']])

json_csv('training')
json_csv('test')