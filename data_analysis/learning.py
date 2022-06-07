import csv
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer


class Learner:

	def __init__(self, dataset_name):
		self.train = pd.read_csv('../data/csv/training.csv').dropna()
		self.df = pd.read_csv('../data/csv/'+ dataset_name +'.csv').dropna()
		self.apply_predictions()


	def bayes(self):
	    return Pipeline(
	        [('vect', TfidfVectorizer(token_pattern=r'[^\s]+', max_features=1700, ngram_range=(1, 2))),
	         ('tfidf', TfidfTransformer()),
	         ('clf', MultinomialNB(
	             alpha=1e-3
	         )
	         )
	        ]
	    )


	def logistic(self):
	    return Pipeline(
	        [('vect', TfidfVectorizer(token_pattern=r'[^\s]+', max_features=30000, ngram_range=(1, 2))),
	         ('tfidf', TfidfTransformer()),
	         ('clf', LogisticRegression(
	             solver='newton-cg',
	             multi_class='multinomial',
	             random_state=42,
	             max_iter=100,
	             class_weight="balanced"
	         )
	         )
	        ]
	    )


	def svm(self):
	    return Pipeline(
	        [('vect', TfidfVectorizer(token_pattern=r'[^\s]+', max_features=26000, ngram_range=(1, 2))),
	         ('tfidf', TfidfTransformer()),
	         ('clf', SGDClassifier(
	             loss='squared_hinge',
	             penalty='l2',
	             alpha=1e-3,
	             random_state=42,
	             learning_rate='optimal',
	             tol=None,
	             class_weight="balanced"
	         )
	         )
	        ]
	    )


	def apply_predictions(self):
		self.df['bayes'] = self.bayes().fit(self.train['text'], self.train['label']).predict(self.df['text'])
		self.df['logistic'] = self.logistic().fit(self.train['text'], self.train['label']).predict(self.df['text'])
		self.df['svm'] = self.svm().fit(self.train['text'], self.train['label']).predict(self.df['text'])
		return True