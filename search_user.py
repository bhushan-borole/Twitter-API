from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import json



with open("twitter_credentials.json", "r") as file:
	creds = json.load(file)

auth = OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_TOKEN_SECRET'])
auth_api = API(auth)

search = input("Enter Username: ")
print("Getting Data For: " + search)

item = auth_api.get_user(screen_name = search)


print("Name: " + item.name)
print("ID: " + str(item.id))
print("Location: " + item.location)
print("Dcreen_name: " + item.screen_name)
print("Description: " + str(item.description))
print("Friends_count: " + str(item.friends_count))
print("Followers_count: " + str(item.followers_count))
print("Created At: " + str(item.created_at))
print("Profile Image Url: " + str(item.profile_image_url))

