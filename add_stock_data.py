import json
import os
import pandas as pd
import yfinance as yf

tickers = ["NVDA", "NFLX", "TSLA","^GSPC"]
colors = ["green", "red", "blue", "purple" ]
deltas = [-7, -5, -3, 0, 3, 5, 7]
ticker_colors = {ticker: color for ticker, color in zip(tickers, colors)}
period = "5y"
tickers_data = {}

def fetch_data(ticker, period):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def fetch_ratio_on_date(ticker, date_str, delta, delta_plus):
    date = pd.to_datetime(date_str, format='%m/%d/%Y')
    desired_date = (date + pd.DateOffset(days=delta + delta_plus)).tz_localize('America/New_York')

    try:
        selected_row = tickers_data[ticker].loc[desired_date]

        opening_price = selected_row['Open']
        closing_price = selected_row['Close']

        #price_delta = closing_price - opening_price

        rolling_average = tickers_data[ticker]['Close'].rolling(window=7).mean().loc[desired_date]

        ratio = (closing_price - rolling_average) / rolling_average
        # print("closing_price " + str(closing_price))
        # print("avg " + str(rolling_average))
        # print("ratio: " + str(ratio) + "\n --------------------------------")
        return ratio

    except KeyError:
      if delta_plus >= 7:
          return None
      else:
          return fetch_ratio_on_date(ticker, date_str, delta, delta_plus + 1)

def dump_data(data):
    output_directory = "final_data_text"
    os.makedirs(output_directory, exist_ok=True)
    for ticket, articles in data.items():
        if articles:
            ticket_file_path = os.path.join(output_directory, f"{ticket}.json")
            with open(ticket_file_path, 'w') as output_file:
                json.dump(articles, output_file, indent=4)
            print(f"Data for {ticket} written to {ticket_file_path}")

def fill_stock_data(data):
    for ticker, color in zip(tickers, colors):
        stock_data = fetch_data(ticker, period)
        tickers_data[ticker] = stock_data

    for ticket in data:
        for article in data[ticket]:
            for delta in deltas:
                if "stock_ratio" not in article:
                    article["stock_ratio"] = {}
                article["stock_ratio"][str(delta)] = fetch_ratio_on_date(ticket.upper(), article["publish_date"], delta, 0)

    dump_data(data)