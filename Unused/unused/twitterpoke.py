# UNUSED

import tweepy
import time
import requests


# https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1 for reference


# Tokens
API_Key = "dFg8cmgBVecgtahmtaK7AfQFR"
API_key_secret = "pJJVtw9JHL9GvhueHwJ3pvgsADNLHpysWMJQmEbXsWsU4LTJDY"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAMZ2WAEAAAAAu65%2FHd61zABkcxfEEeH%2Bw1XWxa4%3DuOM8IoKwnUEN9WFvOZctZZYZKrfFUw34ikUSulbA6n0SNxz1Wq"

# Keys
consumer_key = API_Key
consumer_secret = API_key_secret
access_token = "2435559416-IL5v70QX3RIdxfF6hS9WN3EQJhVFcw3R8vRy9VF"
access_token_secret = "BETOOmAiqxdie9i9xmwsFk8up0wrlRpnsv1snFXBqM75P"

bearer_token = "AAAAAAAAAAAAAAAAAAAAAMZ2WAEAAAAAs7gmbbnPXa2EJKVpfUA42bW6DDg%3DWBR753TzgPs8u1nSP7H5xb25vSDLV6I9LxwLXXGrWKBNlL9K7r"


# Auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


count = 10
text_query = "Pokemon Celebrations Card"

#start_date = '2021-11-01'
#end_date = '2021-11-23'

# URL for seartching "#pokemoncelebrations"
# https://twitter.com/search?q=%23pokemoncelebrations&src=typed_query&f=live

# Modified url for api
url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23pokemoncelebrations&src=typed_query&f=live'


try:
   # Creation of query method using parameters
   tweets = tweepy.Cursor(api.search,q=text_query).items(count)
 
   # Pulling information from tweets iterable object
   tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
 
   # Creation of dataframe from tweets list
   # Add or remove columns as you remove tweet information
   tweets_df = pd.DataFrame(tweets_list)
   tweets_df.to_csv('out.csv')
   
except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)






