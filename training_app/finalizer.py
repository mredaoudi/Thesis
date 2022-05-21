import csv
import json
import time
import tweepy
import datetime


client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAACh0VAEAAAAAW7%2BbhWLfUi6hbWgDPP4slRjDk%2FU%3DcCVxvampJjvIVYNFyLlcMG9BBRvbtXf8BzyzDu6dLXmlg2xPbR')

processed = json.load(open('data/processed.json'))
processed_ids = list(processed.keys())

def transfer_training():
	training = json.load(open('data/training.json'))
	training_ids = list(training.keys())
	remainder = list(set(processed_ids) - set(training_ids))
	for i in remainder:
		print('---------Tweet---------')
		print(i)
		try:
			tweet = client.get_tweet(id=i, tweet_fields=['created_at', 'source', 'entities'], expansions=['author_id'])
			training[i] = {}
			training[i]['previous_processed_text'] = processed[i][0]
			training[i]['sentiment_label'] = processed[i][1]
			if tweet.data != None:
				author = tweet.data.author_id
				user = client.get_user(id=author, user_fields=['created_at', 'location', 'verified'])
				training[i]['tweet_data'] = tweet.data.data
				training[i]['user_data'] = user.data.data
			else:
				training[i]['tweet_data'] = None
				training[i]['user_data'] = None
		except Exception as e:
			print('---------Twitter Timeout---------')
			break
		print('---------Done---------')
	json.dump(training, open("data/training.json", "w"), indent = 4)
	training_ids = list(training.keys())
	return list(set(processed_ids) - set(training_ids))


def error_count(filename):
	obj = json.load(open('data/' + filename + '.json'))
	deleted_count = 0
	count = 0
	for i in obj:
		count += 1
		if obj[i]['user_data'] == None:
			deleted_count += 1
	print(filename + ' --> ' + str(deleted_count) + ' / ' + str(count) + ' = ' + str(deleted_count/count))


def csv_write():
	header = ['text', 'label']
	with open('data/training.csv', 'w', encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerow(['Nouvelle Union Populaire \u00c9cologique et Sociale \u270c\ufe0f', 'pos'])



def transfer_prediction(candidate):
	processed = json.load(open('data/pred_' + candidate + '.json'))
	processed_ids = list(processed.keys())

	prediction = json.load(open('data/prediction_' + candidate + '.json'))
	prediction_ids = list(prediction.keys())
	remainder = list(set(processed_ids) - set(prediction_ids))
	for i in remainder:
		print('---------Tweet---------')
		print(i)
		try:
			tweet = client.get_tweet(id=i, tweet_fields=['created_at', 'source', 'entities'], expansions=['author_id'])
			prediction[i] = {}
			prediction[i]['previous_processed_text'] = processed[i]
			if tweet.data != None:
				author = tweet.data.author_id
				user = client.get_user(id=author, user_fields=['created_at', 'location', 'verified'])
				prediction[i]['tweet_data'] = tweet.data.data
				prediction[i]['user_data'] = user.data.data
			else:
				prediction[i]['tweet_data'] = None
				prediction[i]['user_data'] = None
		except Exception as e:
			print('---------Twitter Timeout---------')
			break
		print('---------Done---------')
	json.dump(prediction, open('data/prediction_' + candidate + '.json', 'w'), indent = 4)
	prediction_ids = list(prediction.keys())
	return list(set(processed_ids) - set(prediction_ids))




error_count('training')
error_count('prediction_macron')
error_count('prediction_lepen')