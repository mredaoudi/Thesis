import csv
import pandas as pd
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

class Lexicons:

	def __init__(self, dataset_name):
		self.df = pd.read_csv('../data/csv/'+ dataset_name +'.csv').dropna()
		self.sia = SentimentIntensityAnalyzer()
		self.apply_predictions()


	def vader_sentiment(self, text):
	    vader_scores = self.sia.polarity_scores(text)
	    if vader_scores['compound'] > 0.05:
	        return 'pos'
	    elif vader_scores['compound'] < -0.05:
	        return 'neg'
	    return 'neu'


	def textblob_sentiment(self, text):
	    textblob_scores = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment
	    if textblob_scores[0] > 0.1:
	        return 'pos'
	    elif textblob_scores[0] < -0.1:
	        return 'neg'
	    return 'neu'


	def apply_predictions(self):
		self.df['vader'] = self.df['text'].apply(self.vader_sentiment)
		self.df['textblob'] = self.df['text'].apply(self.textblob_sentiment)
		return True