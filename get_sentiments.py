import requests
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
            for tweet in data['statuses']:
                sentiment = self.get_sentiment(tweet['text'].translate(non_bmp_map))
                # first tweet of every user
                if tweet['user']['screen_name'] in all_tweets:
                    all_tweets[tweet['user']['screen_name']].append([tweet['text'].translate(non_bmp_map), sentiment])
                # if user exists then append their tweets    
                else: 
                    all_tweets[tweet['user']['screen_name']] = [[tweet['text'].translate(non_bmp_map), sentiment]]
                MAX_ID = tweet['id']

            for i in range(0,30):
                r1 = requests.get(url = url + search + '&count=200&lang=en&max_id=' + str(MAX_ID), auth = self.auth)
                data1 = r1.json()
                for tweet in data1['statuses']:
                    sentiment = self.get_sentiment(tweet['text'].translate(non_bmp_map))
                    # first tweet of every user
                    if tweet['user']['screen_name'] in all_tweets:
                        all_tweets[tweet['user']['screen_name']].append([tweet['text'].translate(non_bmp_map), sentiment])
                    # if user exists then append their tweets 
                    else:
                        all_tweets[tweet['user']['screen_name']] = [[tweet['text'].translate(non_bmp_map), sentiment]]
                    MAX_ID = tweet['id']
            
            return all_tweets

        except Exception as e:
            print(e)



def  main():
    client = Twitter_Client()
    search = input("Enter Keyword: ")

    all_tweets = client.get_tweets(search)

    count_positive = 0
    count_negative = 0
    count_neutral = 0

    for k, v in all_tweets.items():
        for x in v:
            if x[1] == 1:
                count_positive += 1
            elif x[1] == -1:
                count_negative += 1
            else:
                count_neutral += 1

    print('Positive Tweets: {}%'.format(round(count_positive / len(all_tweets) * 100, 2)))
    print('Negative Tweets: {}%'.format(round(count_negative / len(all_tweets) * 100, 2)))
    print('Neutral Tweets: {}%'.format(round(count_neutral / len(all_tweets) * 100, 2)))
    print('Count Of Tweets: {}'.format(len(all_tweets)))

if __name__ == '__main__':
    main()

