import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import date
from datetime import datetime
from datetime import timedelta
import time
import json
from requests_oauthlib import OAuth1
from textblob import TextBlob 
import sys
import re

#reference for non_nmp_map : https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

url = 'https://api.twitter.com/1.1/search/tweets.json?q='

class Twitter_Client:
    def __init__(self):
        try:
            with open("twitter_credentials.json", "r") as file:
                creds = json.load(file)
            self.auth = OAuth1(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
        except Exception as e:
            print(e)



    def get_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0.0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1



    def clean_tweet(self, tweet): 
                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 



    def get_tweets(self, search):
        try:
            all_tweets = {}
            r = requests.get(url = url + search + '&count=200&lang=en', auth = self.auth)
            data = r.json()
            MAX_ID = 0
            Count = 0
            for tweet in data['statuses']:
                text = tweet['text'].translate(non_bmp_map)
                created_at = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                sentiment = self.get_sentiment(text)
                
                if created_at in all_tweets:
                    all_tweets[created_at].append(sentiment)
                else:
                    all_tweets[created_at] = [sentiment]

                #print(all_tweets[created_at])
                
                MAX_ID = tweet['id'] ; Count += 1

            for i in range(0,30):
                r1 = requests.get(url = url + search + '&count=200&lang=en&max_id=' + str(MAX_ID), auth = self.auth)
                data1 = r1.json()

                for tweet in data1['statuses']:
                    text = tweet['text'].translate(non_bmp_map)
                    created_at = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                
                    sentiment = self.get_sentiment(text)
                    #print(sentiment)
                    if created_at in all_tweets:
                        all_tweets[created_at].append(sentiment)
                    else:
                        all_tweets[created_at] = [sentiment]
                    #print(all_tweets[created_at])

                    MAX_ID = tweet['id'] ; Count += 1
            #print(Count)
            average_sentiments = self.group_tweets(all_tweets)
            return average_sentiments
        except Exception as e:
            print(e)



    def get_last_week(self):
        today = date.today()
        l = []
        for i in range(0,7):
            l.append(today - timedelta(days=i))
        return l

    def group_tweets(self, all_tweets):
        last_week = self.get_last_week()
        average_sentiments = {}
        for date in last_week:
        	if str(date) in all_tweets:
        		l = all_tweets[str(date)]
        		#print(l)
        		average_sentiments[date] = sum(l) / len(l)
        return average_sentiments
