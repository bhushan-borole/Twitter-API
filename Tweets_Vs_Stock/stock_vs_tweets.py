from fetch_tweets import Twitter_Client
from nsepy import get_history
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date


def fetch_tweets(company):
    client = Twitter_Client()
    sentiment_data = client.get_tweets(company)
    last_week = client.get_last_week()
    return sentiment_data, last_week


def fetch_stock_data(company, last_week):
    stock_data = get_history(symbol=company, start=last_week[-1], end=last_week[0])
    stock_data = stock_data.reset_index()
    stock_data = stock_data[['Date', 'Close']]
    return stock_data


def plot(sentiment_data, stock_data):
    # converting dictionary into lists of lists
    dictlist = []
    for key, value in sentiment_data.items():
        temp = [key, value]
        dictlist.append(temp)

    sentiment_data = pd.DataFrame(dictlist, columns=['Date', 'Sentiment'])

    stock_data = pd.merge(stock_data, sentiment_data, on='Date', how='left')
    stock_data['Sentiment'] = stock_data['Sentiment'].fillna(99)

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    plt.plot(stock_data['Date'], stock_data['Close'], color='#000000', linewidth=2.0)

    dates_pos = []
    sentiment_pos = []
    dates_neg = []
    sentiment_neg = []
    dates_neu = []
    sentiment_neu = []

    for value in stock_data.iterrows():
        sentiment = float(value[1]['Sentiment'])
        # print(sentiment)
        date = value[1]['Date']
        close = value[1]['Close']
        if sentiment > 0.2:
            dates_pos.append(date)
            sentiment_pos.append(close)
        elif 0.2 > sentiment > -0.2:
            dates_neu.append(date)
            sentiment_neu.append(close)
        elif sentiment < -0.2:
            dates_neg.append(date)
            sentiment_neg.append(close)

    plt.scatter(dates_pos, sentiment_pos, color='#00ff00', marker='^', linewidth=2.0)
    plt.scatter(dates_neg, sentiment_neg, color='#ff0000', marker='v', linewidth=2.0)
    plt.scatter(dates_neu, sentiment_neu, color='#0000ff', marker='.', linewidth=2.0)
    plt.show()


def main():
    company = input("Enter Company Name:")
    sentiment_data, last_week = fetch_tweets(company)
    stock_data = fetch_stock_data(company, last_week)
    plot(sentiment_data, stock_data)


if __name__ == '__main__':
    main()
