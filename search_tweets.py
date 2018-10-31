from twython import Twython
import json

'''
Run this script first to enter your credentials into a json file

import json

# Enter your keys/secrets as strings in the following fields
credentials = {}  
credentials['CONSUMER_KEY'] = ...  
credentials['CONSUMER_SECRET'] = ...  
credentials['ACCESS_TOKEN'] = ...  
credentials['ACCESS_SECRET'] = ...

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)
'''

#opens the above created json file and loads into creds
with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

search = input("Enter keyword: ")

query = {
	'q' : search,
	'result_type' : 'popular',
	'count' : 10,
	'lang' : 'en'
}

dict_ = {'user' : [], 'date' : [], 'text' : []}

for status in python_tweets.search(**query)['statuses']:
	dict_['user'].append(status['user']['screen_name'])
	dict_['date'].append(status['created_at'])
	dict_['text'].append(status['text'])


for i in range(len(dict_['user'])):
        print('User: ', end=' ')
        print(dict_['user'][i])
        print('Date: ', end=' ')
        print(dict_['date'][i])
        print('Text: ', end=' ')
        print(dict_['text'][i])
        print('----------------------------------')
                

