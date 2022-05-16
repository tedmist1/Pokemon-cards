from datetime import datetime

start_date = datetime(2021, 10, 24) # IDK why this has to be 23 and not 24. Need to revisit this.
end_date = datetime(2022, 3, 6)

# The numbers need to match above except for the offset. This offset determines which day you're comparing to which (for predictions in prices)
# For example, offset_days=1 means the prices on 10/25 will be compared to the tweet volume on 10/24
offset_days = 0
start_date_process = datetime(2021, 10, 24+offset_days)
end_date_process = datetime(2022, 3, 6+offset_days)






# Price variables
NUMBER_OF_LINES = 21324 # MANUAL: Update this value This  number needs to manually be updated ot match how many lines your extension file has for price data (usually etb.txt)
date_price_bool = False # If this is true, then when running process.py it generates a graph comparing date to price. 
date_quantity_bool = False # If True, it generates date to quantity sold. Cannot be true when date_price is true
correlation_generate = True




#Twitter processing variables. T
filter = True # if filter is on, then remove all tweets before october
# num_tweets = 17838//2 # The number of tweets we're going through (number of lines divided by 2 floored, since each tweet is two lines)

num_tweets = 44530//5# MANUAL: Update this value
twitter_graphing_extension='tweet_likeretweetreply.txt' # Needs to be updated whenever we change the extension

# num_tweets = 17808//2
# twitter_graphing_extension = 'tweet_data.txt'
relative_path = ''

# These impact graphing.py file and what it graphs
use_likes = False # Maximum of 1 out of these 4 can be true
use_retweets = False
use_replies = False
use_sum = False

lag_correlation = True

likeretweetreply = True # Writes the variables for building a model. Must be true if any of the 4 above are true

# Twitter Scraping Variables
tags = ['PokemonCelebrations']
limitItems = False
maximumItems = 10
trackingPopularityPerTweet = False # Take each tweet and add its likes, retweets, and replies as an additional "hit" for that day
use_followers = False





# Model Variables
multiple_models = True
normalize_terms = False # Cannot normalize if using old days?
use_old_days = False
num_of_shift_days = 7

# Autocorr variables
show_autocorr = False
shift_days = 7 # No longer used?
persistence_autoregression_model = True