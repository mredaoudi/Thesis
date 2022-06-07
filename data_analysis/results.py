import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def accuracy(x, y, cm=True):
    acc = accuracy_score(x, y) * 100
    f1 = f1_score(x, y, average='weighted') * 100
    precision = precision_score(x, y, average='weighted', labels=['pos', 'neu', 'neg']) * 100
    recall = recall_score(x, y, average='weighted', labels=['pos', 'neu', 'neg']) * 100
    if cm:
        print("Accuracy: {:.3f}\nMacro F1-score: {:.3f}\nPrecision: {:.3f}\nRecall: {:.3f}".format(acc, f1, precision, recall))
        print(creport(x, y))
        print(cmatrix(x, y))
        return True
    return {"accuracy": acc, "f1": f1}


def creport(x, y):
    return classification_report(x, y, labels=['pos', 'neu', 'neg'], target_names=['Positive', 'Neutral', 'Negative'])


def cmatrix(x, y):
    cm = confusion_matrix(x, y, labels=['pos', 'neu', 'neg'])
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['pos', 'neu', 'neg'])
    return disp.plot(cmap=plt.cm.YlOrBr)


def outcome(df, column, candidate_amount=None, opponent_amount=None, test=False):
    df = df.groupby(column).count()
    df['percent'] = ((df['text'] / df['text'].sum()) * 100).round(2)
    neg = df.iloc[0]['text']
    neu = df.iloc[1]['text']
    pos = df.iloc[2]['text']
    print(df)
    if not test:
        popularity = (pos / (pos + neg)) * (candidate_amount / (candidate_amount + opponent_amount))
        print(popularity)
    return None