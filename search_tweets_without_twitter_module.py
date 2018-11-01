import requests
import json
from requests_oauthlib import OAuth1


with open("twitter_credentials.json", "r") as file:
	creds = json.load(file)

auth = OAuth1(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

search = input("Enter Keyword: ")

r = requests.get(url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search, auth = auth)

data = r.json()

for tweets in data['statuses']:
        print('User: ' + tweets['user']['screen_name'])
        print('Created At: ' + tweets['created_at'])
        print('Text: ' + tweets['text'])
        print('-----------------------------------------------------------------------------')
