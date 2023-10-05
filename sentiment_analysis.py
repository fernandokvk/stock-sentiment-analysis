import json
import os
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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

# List of JSON files
file_paths = [
    "ticket_data_files/nflx.json",
    "ticket_data_files/tsla.json",
    "ticket_data_files/nvda.json"
]


def load_files(json_file):
    ticket = json_file.split("/")[-1].split(".json")[0]
    with open(json_file, 'r', encoding='utf-8') as file:  # Specify the encoding
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


for ticket in ticket_data:
    for article in ticket_data[ticket]:
        vader_score_raw = parse_text(article['text'])
        scored_article = {
            'title': article['title'],
            'publish_date': article['publish_date'],
            'vader_score_raw': vader_score_raw
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
