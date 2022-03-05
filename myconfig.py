from datetime import datetime

start_date = datetime(2021, 10, 24) # IDK why this has to be 23 and not 24. Need to revisit this.
end_date = datetime(2022, 2, 4)

# The numbers need to match above except for the offset. This offset determines which day you're comparing to which (for predictions in prices)
# For example, offset_days=1 means the prices on 10/25 will be compared to the tweet volume on 10/24
offset_days = 1
start_date_process = datetime(2021, 10, 24+offset_days)
end_date_process = datetime(2022, 2, 4+offset_days)






#Twitter processing variables
filter = True # if filter is on, then remove all tweets before october
# num_tweets = 17838//2 # The number of tweets we're going through (number of lines divided by 2 floored, since each tweet is two lines)
num_tweets = 26822//3
twitter_graphing_extension='tweet_follower.txt'
relative_path = ''





# Price variables
NUMBER_OF_LINES = 20844 # This  number needs to manually be updated ot match how many lines your extension file has for price data (usually etb.txt)
date_price_bool = False # If this is true, then when running process.py it generates a graph comparing date to price. 
date_quantity_bool = False # If True, it generates date to quantity sold. Cannot be true when date_price is true
correlation_generate = True






# Twitter Scraping Variables
hashtag = ['#PokemonCelebrations']
limitItems = False
maximumItems = 10
trackingPopularityPerTweet = False # Take each tweet and add its likes, retweets, and replies as an additional "hit" for that day
use_followers = True