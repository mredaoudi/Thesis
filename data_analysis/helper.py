import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay


def accuracy(df):
    acc = accuracy_score(df['label'], df['pred']) * 100
    f1 = f1_score(df['label'], df['pred'], average='macro') * 100
    print("Accuracy: {:.3f}\nMacro F1-score: {:.3f}".format(acc, f1))
    return cmatrix(df['label'], df['pred'])


def cmatrix(label, pred):
    cm = confusion_matrix(label, pred, labels=['pos', 'neu', 'neg'])
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['pos', 'neu', 'neg'])
    return disp.plot(cmap=plt.cm.YlOrBr)