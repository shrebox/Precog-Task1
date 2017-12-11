import tweepy
import sys
import jsonpickle
import os
import json
from pymongo import MongoClient


#Pass our consumer key and consumer secret to Tweepy's user authentication handler
auth = tweepy.AppAuthHandler("", "")

#Pass our access token and access secret to Tweepy's user authentication handler
#auth.set_access_token("95414066-ajgQtzpOs0CoD2EKE06CHeKw7uiFNoxejeLuCWl0Y", "tsfKPKlRYPiyTZ6tJxEwIhYpMnFfQs69QSgMWsOy02kir")

#Creating a twitter API wrapper using tweepy
#Details here http://docs.tweepy.org/en/v3.5.0/api.html
api = tweepy.API(auth,wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)

# Replace the API_KEY and API_SECRET with your application's key and secret.
#auth = tweepy.AppAuthHandler("", "")

#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# Continue with rest of code

searchQuery = '#Okchi#Mumbai'  # this is what we're searching for
maxTweets = 12000# Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
#fName = 'fakenews.json' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L

#MONGO_HOST= 'mongodb://localhost/twitterdb' 
client = MongoClient()
db = client.precog
tweets = db.MumbaiRains

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

with open('okchi_mumbai.json', 'w') as f:

    all_users = []
    #Tell the Cursor method that we want to use the Search API (api.search)
    #Also tell Cursor our query, and the maximum number of tweets to return
    for tweet in tweepy.Cursor(api.search,q=searchQuery+" -filter:retweets",lang="en").items(maxTweets) :         
        if tweet._json['user']['id']:
            user_id = tweet._json['user']['id']
            if user_id not in all_users:
                all_users.append(user_id)
                #Write the JSON format to the text file, and add one to the number of tweets we've collected
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
                tweets.insert_one(tweet._json)
                tweetCount += 1
                print("Downloaded {0} tweets".format(tweetCount))

    #Display how many tweets we have collected
    print("Downloaded {0} tweets finally".format(tweetCount))
