import os
import json
from newspaper import Article

ticket_data = {}

file_paths = [
    "data/netflix.json",
    "data/tesla.json",
    "data/nvidia.json"
]


def download_and_parse_articles(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    articles = data.get('articles', [])

    for article_data in articles:
        url = article_data.get('url')
        if url:
            try:
                article = Article(url)
                article.download()
                article.parse()

                article_info = {
                    'title': article.title,
                    'publish_date': article_data.get('publish_date'),
                    'text': article.text
                }

                ticket = data['ticket']
                if ticket not in ticket_data:
                    ticket_data[ticket] = []

                ticket_data[ticket].append(article_info)

            except Exception as e:
                print(f"Error processing {url}: {str(e)}")


for file_path in file_paths:
    download_and_parse_articles(file_path)


output_directory = "ticket_data_files"
os.makedirs(output_directory, exist_ok=True)

for ticket, articles in ticket_data.items():
    if articles:
        ticket_file_path = os.path.join(output_directory, f"{ticket}.json")
        with open(ticket_file_path, 'w') as output_file:
            json.dump(articles, output_file, indent=4)
        print(f"Data for {ticket} written to {ticket_file_path}")

# Error processing https://www.wsj.com/articles/netflix-to-spend-100-million-to-help-underrepresented-communities-in-entertainment-11614348003: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-to-spend-100-million-to-help-underrepresented-communities-in-entertainment-11614348003 on URL https://www.wsj.com/articles/netflix-to-spend-100-million-to-help-underrepresented-communities-in-entertainment-11614348003
# Error processing https://www.wsj.com/articles/netflix-raises-prices-on-u-s-canada-plans-11642196773: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-raises-prices-on-u-s-canada-plans-11642196773 on URL https://www.wsj.com/articles/netflix-raises-prices-on-u-s-canada-plans-11642196773
# Error processing https://www.wsj.com/articles/netflix-tops-200-million-subscribers-for-the-first-time-11611090902: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-tops-200-million-subscribers-for-the-first-time-11611090902 on URL https://www.wsj.com/articles/netflix-tops-200-million-subscribers-for-the-first-time-11611090902
# Error processing https://www.wsj.com/articles/netflix-facing-reality-check-subscriber-loss-stock-plummet-cut-costs-vows-to-curb-its-profligate-ways-11650547424: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-facing-reality-check-subscriber-loss-stock-plummet-cut-costs-vows-to-curb-its-profligate-ways-11650547424 on URL https://www.wsj.com/articles/netflix-facing-reality-check-subscriber-loss-stock-plummet-cut-costs-vows-to-curb-its-profligate-ways-11650547424
# Error processing https://www.wsj.com/articles/netflix-stock-price-plunges-premarket-after-subscriber-loss-11650449002: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-stock-price-plunges-premarket-after-subscriber-loss-11650449002 on URL https://www.wsj.com/articles/netflix-stock-price-plunges-premarket-after-subscriber-loss-11650449002
# Error processing https://www.wsj.com/articles/netflix-earnings-q1-2022-11650325682: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-earnings-q1-2022-11650325682 on URL https://www.wsj.com/articles/netflix-earnings-q1-2022-11650325682
# Error processing https://www.wsj.com/articles/netflix-password-sharing-crackdown-how-11650488569: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-password-sharing-crackdown-how-11650488569 on URL https://www.wsj.com/articles/netflix-password-sharing-crackdown-how-11650488569
# Error processing https://www.wsj.com/articles/netflix-with-ads-launching-as-talks-continue-with-studios-over-content-11667381403: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-with-ads-launching-as-talks-continue-with-studios-over-content-11667381403 on URL https://www.wsj.com/articles/netflix-with-ads-launching-as-talks-continue-with-studios-over-content-11667381403
# Error processing https://www.wsj.com/articles/netflix-ads-to-launch-in-november-11665680110: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-ads-to-launch-in-november-11665680110 on URL https://www.wsj.com/articles/netflix-ads-to-launch-in-november-11665680110
# Error processing https://www.wsj.com/articles/netflix-nflx-q3-earnings-report-2022-11666056348: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-nflx-q3-earnings-report-2022-11666056348 on URL https://www.wsj.com/articles/netflix-nflx-q3-earnings-report-2022-11666056348
# Error processing https://www.wsj.com/articles/netflix-seeks-ways-to-get-subscribers-to-return-after-visits-decline-11666032658: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/netflix-seeks-ways-to-get-subscribers-to-return-after-visits-decline-11666032658 on URL https://www.wsj.com/articles/netflix-seeks-ways-to-get-subscribers-to-return-after-visits-decline-11666032658
# Error processing https://www.wsj.com/articles/tesla-tops-volkswagen-to-become-second-most-valuable-auto-maker-11579709320: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/tesla-tops-volkswagen-to-become-second-most-valuable-auto-maker-11579709320 on URL https://www.wsj.com/articles/tesla-tops-volkswagen-to-become-second-most-valuable-auto-maker-11579709320
# Error processing https://www.wsj.com/articles/tesla-posts-fourth-quarter-profit-on-record-deliveries-11580334615: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/tesla-posts-fourth-quarter-profit-on-record-deliveries-11580334615 on URL https://www.wsj.com/articles/tesla-posts-fourth-quarter-profit-on-record-deliveries-11580334615
# Error processing https://www.wsj.com/articles/tesla-stock-elon-musk-electric-vehicle-11673623093: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/tesla-stock-elon-musk-electric-vehicle-11673623093 on URL https://www.wsj.com/articles/tesla-stock-elon-musk-electric-vehicle-11673623093
# Error processing https://www.wsj.com/articles/elon-musks-decision-to-slow-new-tesla-models-risks-holding-up-growth-11643375015: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/elon-musks-decision-to-slow-new-tesla-models-risks-holding-up-growth-11643375015 on URL https://www.wsj.com/articles/elon-musks-decision-to-slow-new-tesla-models-risks-holding-up-growth-11643375015
# Error processing https://finance.yahoo.com/news/does-nvidias-nasdaq-nvda-p-123227974.html  : Article `download()` failed with 404 Client Error: Not Found for url: https://finance.yahoo.com/news/does-nvidias-nasdaq-nvda-p-123227974.html%20%20 on URL https://finance.yahoo.com/news/does-nvidias-nasdaq-nvda-p-123227974.html
# Error processing https://www.wsj.com/articles/nvidia-nvda-q1-earnings-report-2024-132e3559: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/nvidia-nvda-q1-earnings-report-2024-132e3559 on URL https://www.wsj.com/articles/nvidia-nvda-q1-earnings-report-2024-132e3559
# Error processing https://www.wsj.com/articles/nvidia-stocks-surge-makes-chip-maker-10th-biggest-u-s-listed-company-11626696001: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/nvidia-stocks-surge-makes-chip-maker-10th-biggest-u-s-listed-company-11626696001 on URL https://www.wsj.com/articles/nvidia-stocks-surge-makes-chip-maker-10th-biggest-u-s-listed-company-11626696001
# Error processing https://www.wsj.com/articles/nvidia-posts-record-revenue-as-videogaming-sales-soar-11637185887: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/nvidia-posts-record-revenue-as-videogaming-sales-soar-11637185887 on URL https://www.wsj.com/articles/nvidia-posts-record-revenue-as-videogaming-sales-soar-11637185887
# Error processing https://www.wsj.com/articles/nvidia-posts-record-sales-as-pandemic-sustains-demand-for-gaming-data-center-chips-11597871110: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/nvidia-posts-record-sales-as-pandemic-sustains-demand-for-gaming-data-center-chips-11597871110 on URL https://www.wsj.com/articles/nvidia-posts-record-sales-as-pandemic-sustains-demand-for-gaming-data-center-chips-11597871110
# Error processing https://www.wsj.com/articles/how-nvidias-ceo-cooked-up-americas-biggest-semiconductor-company-11600184856: Article `download()` failed with 403 Client Error: Forbidden for url: https://www.wsj.com/articles/how-nvidias-ceo-cooked-up-americas-biggest-semiconductor-company-11600184856 on URL https://www.wsj.com/articles/how-nvidias-ceo-cooked-up-americas-biggest-semiconductor-company-11600184856