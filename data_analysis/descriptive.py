import re
import csv
import json
import emoji
from helper import preprocess 
import numpy as np
import pandas as pd
from datetime import datetime as dt

class DataSet:

	def __init__(self, dataset_name):
		self.dataset = json.load(open('../data/json/' + dataset_name + '.json'))


	def get_labels(self):
	    tweet_ids = []
	    labels = []
	    
	    for tweet, details in self.dataset.items():
	        tweet_ids.append(tweet)
	        labels.append(details['sentiment_label'])
	    return pd.DataFrame({'Tweet ID': tweet_ids, 'Sentiment': labels})


	def get_tags(self, tag_type):
	    tag_identifier = 'tag' if tag_type == 'hashtags' else 'username'
	    tweet_ids = []
	    tweet_tags = []
	    
	    for tweet, details in self.dataset.items():
	        if (details['tweet_data'] and
	            ('entities' in details['tweet_data']) and
	            (tag_type in details['tweet_data']['entities'])):
	            for tag in details['tweet_data']['entities'][tag_type]:
	                tweet_ids.append(tweet)
	                tweet_tags.append(tag[tag_identifier])
	        else:
	            tweet_ids.append(tweet)
	            tweet_tags.append(None)
	    return pd.DataFrame({'Tweet ID': tweet_ids, tag_type.capitalize(): tweet_tags})


	def get_sources(self):
	    tweet_ids = []
	    tweet_sources = []
	    
	    for tweet, details in self.dataset.items():
	        tweet_ids.append(tweet)
	        tweet_sources.append(details['tweet_data']['source'] if details['tweet_data'] else None)
	    return pd.DataFrame({'Tweet ID': tweet_ids, 'Source': tweet_sources})


	def get_verifications(self):
	    tweet_ids = []
	    users_is_verified = []
	    
	    for tweet, details in self.dataset.items():
	        tweet_ids.append(tweet)
	        users_is_verified.append(details['user_data']['verified'] if details['user_data'] else None)
	    return pd.DataFrame({'Tweet ID': tweet_ids, 'User Verified': users_is_verified})


	def calculate_time_difference(self):
	    tweet_ids = []
	    time_difference = []
	    
	    for tweet, details in self.dataset.items():
	        tweet_ids.append(tweet)
	        if details['tweet_data']:
	            user_created_at = dt.strptime(details['user_data']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
	            tweet_created_at = dt.strptime(details['tweet_data']['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
	            time_diff = tweet_created_at - user_created_at
	            time_difference.append(time_diff.days)
	        else:
	            time_difference.append(None)

	    return pd.DataFrame({'Tweet ID': tweet_ids, 'Time Difference': time_difference})


	def get_words(self):
	    tweet_ids = []
	    words = []
	    
	    for tweet, details in self.dataset.items():
	        sentence = details['tweet_data']['text'] if details['tweet_data'] else details['previous_processed_text']
	        tokens = sentence.split()
	        for t in tokens:
	            if re.match(r'[^\W\d]*$', t):
	                tweet_ids.append(tweet)
	                words.append(t)
	    return pd.DataFrame({'Tweet ID': tweet_ids, 'Word': words})


	def get_character_count(self):
	    tweet_ids = []
	    tweet_char_counter = []
	    
	    for tweet, details in self.dataset.items():
	        tweet_ids.append(tweet)
	        if details['tweet_data']:
	            # Remove links
	            text = re.sub(r'http\S+', '', details['tweet_data']['text'])
	            tweet_char_counter.append(len(text))
	        else:
	            tweet_char_counter.append(np.nan)
	        
	    return pd.DataFrame({'Tweet ID': tweet_ids, 'Character Count': tweet_char_counter})


	def get_emojis(self):
	    tweet_ids = []
	    emojis = []
	    
	    for tweet, details in self.dataset.items():
	        if details['tweet_data']:
	            previous_char = ''
	            for char in details['tweet_data']['text']:
	            	if char == '🇫':
	            		previous_char = char
	            	elif char == '🇷' and previous_char == '🇫':
	            		tweet_ids.append(tweet)
	            		emojis.append('🇫🇷')
	            		previous_char = ''
	            	elif char in emoji.UNICODE_EMOJI['fr']:
	            		tweet_ids.append(tweet)
	            		emojis.append(char)
	        
	    return pd.DataFrame({'Tweet ID': tweet_ids, 'Emoji': emojis})

