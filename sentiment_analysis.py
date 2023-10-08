import json
import os
import nltk
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import add_stock_data

nltk.download('wordnet')
nltk.download('stopwords')

ticket_data = {
    'nflx': [],
    'tsla': [],
    'nvda': []
}

file_paths = [
    "ticket_data_files/nflx.json",
    "ticket_data_files/tsla.json",
    "ticket_data_files/nvda.json"
]


def load_files(json_file):
    ticket = json_file.split("/")[-1].split(".json")[0]
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for article in data:
        article_info = {
            'title': article['title'],
            'publish_date': article['publish_date'],
            'text': article['text']
        }
        ticket_data[ticket].append(article_info)


for files in file_paths:
    load_files(files)

def stem_text(article):
    stemmer = PorterStemmer()
    raw_text = article['text']
    stemmed_text = ' '.join([stemmer.stem(word) for word in raw_text.split()])
    article['text_stemmed'] = stemmed_text

def remove_stopwords(article):
    stop_words = set(stopwords.words('english'))
    raw_text = article['text']
    text_without_stopwords = ' '.join([word for word in raw_text.split() if word.lower() not in stop_words])
    article['text_without_stopwords'] = text_without_stopwords

def lemmatize(article):
    lemmatizer = WordNetLemmatizer()
    raw_text = article['text']
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word) for word in raw_text.split()])
    article['text_lemmatized'] = lemmatized_text

for ticket in ticket_data:
    for article in ticket_data[ticket]:
        lemmatize(article)
        stem_text(article)
        remove_stopwords(article)

def parse_text(text):
    vader_analyzer = SentimentIntensityAnalyzer()
    result =  vader_analyzer.polarity_scores(text)
    # blob = TextBlob(text)
    # sentiment = blob.sentiment
    # result = {
    #     "compound": sentiment.polarity
    # }
        return result

scored_data = {
    'nflx': [],
    'tsla': [],
    'nvda': []
}

for ticket in ticket_data:
    for article in ticket_data[ticket]:
        vader_score_raw = parse_text(article['text'])
        vader_score_lemmatized = parse_text(article['text_lemmatized'])
        vader_score_steemed = parse_text(article['text_stemmed'])
        vader_score_without_stopwords = parse_text(article['text_without_stopwords'])
        scored_article = {
            'title': article['title'],
            'publish_date': article['publish_date'],
            'vader_score_raw': vader_score_raw,
            'vader_score_lemmatized': vader_score_lemmatized,
            'vader_score_steemed': vader_score_steemed,
            'vader_score_stopwords': vader_score_without_stopwords
        }
        scored_data[ticket].append(scored_article)

add_stock_data.fill_stock_data(scored_data)
