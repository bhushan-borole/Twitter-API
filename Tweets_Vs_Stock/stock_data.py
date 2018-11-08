from tweets_vs_stock import Twitter_Client
from nsepy import get_history
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date

client = Twitter_Client()
company = input("Enter Company Name: ")
sentiment_data = client.get_tweets(company)
print(sentiment_data)
last_week = client.get_last_week()

stock_data = get_history(symbol = company, start = last_week[-1], end = last_week[0])
stock_data = stock_data.reset_index()
stock_data = stock_data[['Date', 'Close']]
print(stock_data)
sentiment_data = pd.DataFrame(sentiment_data.items(), columns = ['Date', 'Sentiment'])
print(sentiment_data)
sentiment_data['Date'] = sentiment_data['Date'].apply(lambda x: datetime.date(int(x.split('/')[2]),int(x.split('/')[0]),int(x.split('/')[1])))
print(sentiment_data['Date'])
stock_data = pd.merge(stock_data,sentiment_data,on='Date',how='left')
stock_data['Sentiment'] = stock_data['Sentiment'].fillna(99)

fig, ax = plt.subplots(1, 1, figsize=(10, 5))
plt.plot(stock_data['Date'],stock_data['Close'], color='#000000', linewidth=2.0)

dates_pos = []
sentiment_pos = []
dates_neg = []
sentiment_neg = []
dates_neu = []
sentiment_neu = []

for value in stock_data.iterrows():
	sentiment = int(value[1]['Sentiment'])
	print(sentiment)
	date = value[1]['Date']
	close = value[1]['Close']
	if sentiment == 1:
		dates_pos.append(date)
		sentiment_pos.append(close)
	elif sentiment == 0:
		dates_neu.append(date)
		sentiment_neu.append(close)
	elif sentiment == -1:
		dates_neg.append(date)
		sentiment_neg.append(close)
print(dates_pos)
print(sentiment_pos)
print(dates_neg)
print(sentiment_neg)
print(dates_neu)
print(sentiment_neu)


plt.scatter(dates_pos, sentiment_pos,color='#00ff00',marker='^',linewidth=2.0)
plt.scatter(dates_neg, sentiment_neg,color='#ff0000',marker='v',linewidth=2.0)
# plt.scatter(dates_neu, sentiment_neu,color='#0000ff',marker='.',linewidth=2.0)
plt.show()