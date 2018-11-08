# Twitter API

- This repository is my basic project to integrate Twitter API with python.

- Before using these files make sure you have created a twitter app. If not click here [Twitter App](https://apps.twitter.com/ "Twitter App")

Run this script first to enter your credentials into a json file

```python
import json

#Enter your keys/secrets as strings in the following fields

credentials = {}  
credentials['CONSUMER_KEY'] = ...  
credentials['CONSUMER_SECRET'] = ...  
credentials['ACCESS_TOKEN'] = ...  
credentials['ACCESS_SECRET'] = ...

#Save the credentials object to file

with open("twitter_credentials.json", "w") as file:  
    json.dump(credentials, file)
```

1) Search Tweets with twitter module based on a keyword:

	```python
	python search_tweets.py
	```

2) Search Tweets without twitter module based on a keyword:
	
	```python
	python search_tweets_without_twitter_module.py
	```

3) Search Tweets of a particular user:
	
	```python
	# input must me twitter username, of that particular user
	python get_user's_tweets.py
	```

4) Search details of a particular user:
	
	```python
	# input must me twitter username, of that particular user
	python get_user.py
	```

5) Get the percentage of positive, negative and neutral tweets based on a keyword:
	
	```python
	python get_sentiments.py
	```

6) Plot sentiments of tweets alongwith company's closing prices for a particular week:
	
	```python
	python stock_vs_tweets.py
	```