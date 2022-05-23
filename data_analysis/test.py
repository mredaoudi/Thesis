import json
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer


SIA = SentimentIntensityAnalyzer()


# Extract json into dictionary
def load_json_data(dataset_name):
	return json.load(open('../data/' + dataset_name + '.json'))


def preprocess_tweet(tweet_text):
	return tweet_text


def get_labels_rule_based(tweet_text):
    vader_scores = SIA.polarity_scores(tweet_text)
    if vader_scores['compound'] > 0.05:
        vader_label = 'pos'
    elif vader_scores['compound'] < -0.05:
        vader_label = 'neg'
    else:
        vader_label = 'neu'
    textblob_scores = TextBlob(tweet_text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment
    if textblob_scores[0] > 0.1:
        textblob_label = 'pos'
    elif textblob_scores[0] < -0.1:
        textblob_label = 'neg'
    else:
        textblob_label = 'neu'
    return (vader_label, textblob_label)


def rule_based_sentiment(dataset_name):
    dataset = load_json_data(dataset_name)
    tweet_texts = []
    vader_labels = []
    textblob_labels = []
    
    for tweet, details in dataset.items():
        if details['tweet_data']:
            processed_text = preprocess_tweet(details['tweet_data']['text'])
        else:
            processed_text = details['previous_processed_text']
        tweet_texts.append(processed_text)
        rule_based_labels = get_labels_rule_based(processed_text)
        vader_labels.append(rule_based_labels[0])
        textblob_labels.append(rule_based_labels[1])
        print(tweet + '  -- Done')
        
    return pd.DataFrame({'Tweet Text': tweet_texts, 'VADER Labels': vader_labels, 'TextBlob Labels': textblob_labels})
            
print(rule_based_sentiment('training'))

