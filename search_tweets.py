from twython import Twython
import json
import sys

#reference for non_nmp_map : https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

search = input("Enter keyword: ")
max_attempts = int(input("Enter Max Attempts: "))

COUNT = 1000
tweets = {}

#----------------------------------------------------------------#
# STEP 1: Query Twitter
# STEP 2: Save the returned tweets
# STEP 3: Get the next max_id
#----------------------------------------------------------------#

for i in range(0, max_attempts):
        if COUNT < len(tweets):
            break

        if i == 0:
            results = python_tweets.search(q = search, count = '100')
        else:
            results = python_tweets.search(q = search, include_entities = 'true', max_id = next_max_id)

        
        for result in results['statuses']:
            tweets[result['user']['screen_name']] = result['text'].translate(non_bmp_map)


        try:
            next_results_url_params = results['search_metadata']['next_results']
            next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]  
        except:
            break


for k, v in tweets.items():
    print("User: " + k)
    print("Tweet: " + v)
    print(''.join(['-']*15))
    
print(str(len(tweets)) + " tweets fetched.")
