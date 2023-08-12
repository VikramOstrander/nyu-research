# ------------
# program to analyze performce of sentiment analysis
# confusion matrix saved in data/visualizations/confusion_matrix.png
# model accuracy: 97.38%
# ------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

# import data
data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\review_sentiments.csv")
df = pd.DataFrame(data)

# generate columns to compare sentiments and numerical ratings
# numerical ratings greater than 3 are considered positive, 3 and below are consider negative
df['Count_Sentiment'] = np.where(df['Sentiment'] == 'POSITIVE', 1, 0)
df['Count_Review'] = np.where(df['Rating'] > 3, 1, 0)

# print accuracy score
print(f"accuracy: {metrics.accuracy_score(df['Count_Review'], df['Count_Sentiment'])}")

# print f-score
print(f"f-score: {metrics.f1_score(df['Count_Review'], df['Count_Sentiment'])}")

# generate and show confusion matrix
confusion_matrix = metrics.confusion_matrix(df['Count_Review'], df['Count_Sentiment'])
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix, display_labels = ['Negative', 'Positive'])
cm_display.plot(values_format='', cmap="Blues")
cm_display.ax_.set(title='Confusion Matrix', xlabel='Predicted Sentiment', ylabel='Actual Sentiment')
plt.show()
