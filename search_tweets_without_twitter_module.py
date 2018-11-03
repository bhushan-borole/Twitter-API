import requests
import json
import ast
from requests_oauthlib import OAuth1

import sys

#reference for non_nmp_map : https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


with open("twitter_credentials.json", "r") as file:
	creds = json.load(file)

auth = OAuth1(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

search = input("Enter Keyword: ")

r = requests.get(url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + search, auth = auth)

data = r.json()

for tweets in data['statuses']:
        print('User: ' + tweets['user']['screen_name'])
        print('Created At: ' + tweets['created_at'])
        print('Text: ' + tweets['text'].translate(non_bmp_map))
        print('-----------------------------------------------------------------------------')

        
