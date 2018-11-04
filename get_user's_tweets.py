import tweepy #https://github.com/tweepy/tweepy
import sys
import json
import csv

#reference for non_nmp_map : https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)


def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
    auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    
    alltweets = []  
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #update the new tweets into the list
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.user, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
        
    for tweet in alltweets:
        print(str(alltweets.index(tweet) + 1) + '.)')
        print("Created At: " + str(tweet.created_at))
        print("Text: " + tweet.text.translate(non_bmp_map)) 
    # write the csv 
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass




if __name__ == '__main__':
    #pass in the username of the account you want to download
    user = input("Enter the username: ")
    get_all_tweets(user)
