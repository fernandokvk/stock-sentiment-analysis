import json
import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
nltk.download('wordnet')
nltk.download('stopwords')


class ParsedArticle:
    def __init__(self, title, publish_date):
        self.title = title
        self.publish_date = publish_date
        self.scores = {}
    def add_score(self, score_name, score_value):
        self.scores[score_name] = score_value


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


def parse_text(text):
    vader_analyzer = SentimentIntensityAnalyzer()
    return vader_analyzer.polarity_scores(text)


scored_data = {
    'nflx': [],
    'tsla': [],
    'nvda': []
}
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

output_directory = "scored_data"
os.makedirs(output_directory, exist_ok=True)
for ticket, articles in scored_data.items():
    if articles:
        ticket_file_path = os.path.join(output_directory, f"{ticket}.json")
        with open(ticket_file_path, 'w') as output_file:
            json.dump(articles, output_file, indent=4)
        print(f"Data for {ticket} written to {ticket_file_path}")
