# ------------
# program to perform sentiment analysis on textual reviews from reviews.csv
# sentiment analysis performed with 'sentiment' text classifier from flair
# results exported to review_sentiments.csv
# ------------

import pandas as pd
import time
import datetime

from flair.data import Sentence
from flair.nn import Classifier



# -----VALUES TO EDIT-----
START = 0
FINISH = 3122488
BATCH = 10000
# ------------------------



# import data
data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\reviews.csv")
df = pd.DataFrame(data)

# ensure FINISH is not greater than data length
if FINISH > len(df):
    FINISH = len(df)

# load text classifier 'sentiment' from flair
tagger = Classifier.load('sentiment')

# record start time
start_time = time.time()

for i in range(START, FINISH, BATCH):

    # ensure bounds are correct
    END = min(i+BATCH, FINISH)

    # declare empty lists for sentiments and scores
    sentiments = []
    scores = []

    # generate sentiments for current batch
    t = time.time()
    for review in df['Review'][i:END]:

        # predict sentiment and score and append to lists
        sentence = Sentence(str(review))
        tagger.predict(sentence)
        polarity = sentence.labels[0].value
        sentiments.append(polarity)
        if polarity == 'POSITIVE':
            scores.append(round(sentence.labels[0].score,4))
        else:
            scores.append(round(-1*sentence.labels[0].score,4))
    
    # append current batch to review_sentiments.csv
    temp_df = df.iloc[i:END]
    temp_df['Sentiment'] = sentiments
    temp_df['Score'] = scores
    temp_df = temp_df[['Doctor ID', 'Doctor Name', 'Rating', 'Sentiment', 'Score', 'Review']]
    if i == 0:
        temp_df.to_csv('data/review_sentiments.csv', mode='a', index=False, encoding='utf-8')
    else:
        temp_df.to_csv('data/review_sentiments.csv', mode='a', index=False, header=False, encoding='utf-8')
    t = time.time() - t

    # print update to console
    cur_time = str(datetime.timedelta(seconds=round(time.time()-start_time)))
    print('-'*20)
    print(f"processed {END-START} doctors in {cur_time}\ncurrent progress: {END} of {FINISH} done\ncurrent rate: {round(t/BATCH, 6)}")
    print('-'*20)
