from twython import Twython
import json
import sys

#reference for non_nmp_map : https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

class Twitter_Client:
    def __init__(self):
        with open("twitter_credentials.json", "r") as file:
            creds = json.load(file)

        # Instantiate an object
        self.api = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    def get_tweets(self, search, max_attempts, COUNT):
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
                    results = self.api.search(q = search, count = '200')
                else:
                    results = self.api.search(q = search, include_entities = 'true', max_id = next_max_id)

                
                for result in results['statuses']:
                    tweets[result['user']['screen_name']] = result['text'].translate(non_bmp_map)
                    next_max_id = result['id']
        return tweets
                

def main():
    search = input("Enter keyword: ")
    max_attempts = int(input("Enter Max Attempts: "))
    COUNT = 3000
    client = Twitter_Client()
    tweets = client.get_tweets(search, max_attempts, COUNT)

    for k, v in tweets.items():
        print("User: " + k)
        print("Tweet: " + v)
        print(''.join(['-']*15))
        
    print(str(len(tweets)) + " tweets fetched.")


if __name__ == '__main__':
    main()

