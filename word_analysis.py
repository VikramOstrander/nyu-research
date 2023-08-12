# ------------
# program to analyze keywords from textual reviews
# PREPROCESSING:
#       parse data to extract lemminized tokens
#       separate positive and negative reviews for visualizations
#       positive tokens exported to processed_positive_reviews.csv
#       negative tokens exported to processed_negative_reviews.csv
# ANALYSIS:
#       generate frequency distribution charts for all, positive, and negative reviews
#       generate word clouds for all, positive, and negative reviews
#       find the optimal number of topics for LDA
#       generate an LDA model for the optimal number of topics
# ------------

import pandas as pd
import re
import time

import spacy
from nltk.corpus import stopwords

from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

import gensim
from gensim import corpora
from gensim.models import CoherenceModel

import pyLDAvis
import pyLDAvis.gensim_models



# ---PREPROCESSING---
# if performing preprocessing, comment out all ANALYSIS

# import data
data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\review_sentiments.csv")
df = pd.DataFrame(data)
df_pos = df[df.Sentiment == 'POSITIVE']
df_neg = df[df.Sentiment == 'NEGATIVE']
reviews_pos = df_pos['Review']
reviews_neg = df_neg['Review']

# load nltk stopwords and spacy 'en_core_web_sm' model
stop_words = stopwords.words('english')
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# preprocess a set of textual reviews
def preprocess(input):
        output = []
        for review in input:
            parsed_review = []
            review = str(review).replace("[^a-zA-Z#]", " ")
            text = []
            for word in review.split():
                if (word not in stop_words) and (len(word) > 2):
                    text.append(word.lower())
            doc = nlp(' '.join(text))
            for token in doc:
                if token.pos_ in ['NOUN', 'ADJ'] and token.lemma_ != 'doctor':
                    parsed_review.append(token.lemma_)
            output.append(parsed_review)
        return output

# preprocess positive and negative reviews
print("being preprocessing")
t = time.time()
parsed_reviews_pos = preprocess(reviews_pos)
parsed_reviews_neg = preprocess(reviews_neg)
t = time.time() - t
print(f"done preprocessing - total time: {t}")

# export positive lemminized tokens to processed_positive_reviews.csv
processed_df_pos = pd.DataFrame({'Text': parsed_reviews_pos})
processed_df_pos.to_csv('data/processed_positive_reviews.csv', index=False, encoding='utf-8')

# export negative lemminized tokens to processed_negative_reviews.csv
processed_df_neg = pd.DataFrame({'Text': parsed_reviews_neg})
processed_df_neg.to_csv('data/processed_negative_reviews.csv', index=False, encoding='utf-8')

# -------------------



# ---ANALYSIS---
# if performing analysis, comment out all pre-processing

# generate a frequency distribution chart
def freq_words(reviews, title, reorder=True):
    if reorder:
        words = []
        for review in reviews:
            for word in review:
                words.append(word)
    else:
        words = reviews
    fdist = FreqDist(words)
    words_df = pd.DataFrame({'word':list(fdist.keys()), 'count':list(fdist.values())})

    d = words_df.nlargest(columns="count", n=10) 
    plt.figure(figsize=(10,5))
    ax = sns.barplot(data=d, x="word", y="count", palette=sns.color_palette('tab10'))
    ax.set(xlabel='Words', ylabel='Count')
    plt.title(title)
    plt.tight_layout()
    plt.savefig("data/visualizations/freq.png",bbox_inches='tight')
    plt.show()


# generate a word cloud
def word_cloud(reviews, width, height, reorder=True):
    if reorder:
        words = []
        for review in reviews:
            for word in review:
                words.append(word)
    else:
        words = reviews
    words = []
    for review in reviews:
        for word in review:
            words.append(word)
    wordcloud = WordCloud(width=width, height=height, collocations=False).generate(' '.join(words))
    fig=plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


# generate an lda
def lda(reviews, num_topics, visualize=True):
    id2word = corpora.Dictionary(reviews)
    corpus = [id2word.doc2bow(review) for review in reviews]
    LDA = gensim.models.ldamodel.LdaModel
    lda_model = LDA(corpus=corpus, id2word=id2word, num_topics=num_topics, random_state=100, chunksize=1000, passes=3, per_word_topics=True)
    
    print("Calculating Coherence")
    coherence_model_lda = CoherenceModel(model=lda_model, texts=reviews, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print(f'Coherence Score: {coherence_lda}')

    if visualize is True:
        vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
        pyLDAvis.save_html(vis, f'data/visualizations/lda_vis_{num_topics}.html')
        
    return coherence_lda


# generate ldas with varying num_topics and graph their coherence scores
def optimize_lda(reviews):
    start = 4
    step = 1
    limit = 15

    model_list = []
    coherences = []
    for num_topics in range(start, limit, step):
        model_list.append(num_topics)
        coherences.append(lda(reviews, num_topics, False))

    x = range(start, limit, step)
    plt.plot(x, coherences)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherences")
    plt.legend(("coherences"), loc='best')
    plt.show()


def main():

    print('---loading data---')

    # import data
    pos_data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\processed_positive_reviews.csv")
    neg_data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\processed_negative_reviews.csv")
    pos_df = pd.DataFrame(pos_data)
    neg_df = pd.DataFrame(neg_data)
    parsed_reviews_pos = pos_df['Text'].tolist()
    parsed_reviews_neg = neg_df['Text'].tolist()

    for i in range(0, len(parsed_reviews_pos)):
        parsed_reviews_pos[i] = re.sub(r'\W', ' ', str(parsed_reviews_pos[i])).split()
    for i in range(0, len(parsed_reviews_neg)):
        parsed_reviews_neg[i] = re.sub(r'\W', ' ', str(parsed_reviews_neg[i])).split()

    parsed_reviews_total = parsed_reviews_pos
    for review in parsed_reviews_neg:
        parsed_reviews_total.append(review)

    print('---begin analysis---')

    # generate frequency distributions for total, positive, negative
    freq_words(parsed_reviews_total, "Frequency of Words in All Reviews")
    freq_words(parsed_reviews_pos, "Frequency of Words in Positive Reviews")
    freq_words(parsed_reviews_neg, "Frequency of Words in Negative Reviews")

    # generate word clouds for total, positive, negative
    # word_cloud(parsed_reviews_total, 2000, 1000)
    # word_cloud(parsed_reviews_pos, 1000, 1000)
    # word_cloud(parsed_reviews_neg, 1000, 1000)

    # generate lda
    # optimize_lda(parsed_reviews_total)
    # lda(parsed_reviews_total, 6)

if __name__ == "__main__":
    main()

# --------------
