from datetime import datetime

# General Variables - Used for both scraping and analysis

start_date = datetime(2021, 10, 24) # The start date to analyze tweets/price
end_date = datetime(2022, 3, 6) # The last date to analyze tweets/prices

# The numbers need to match above except for the offset. This offset determines which day you're comparing to which (for predictions in prices)
# For example, offset_days=1 means the prices on 10/25 will be compared to the tweet volume on 10/24
offset_days = 0
start_date_process = datetime(2021, 10, 24+offset_days)
end_date_process = datetime(2022, 3, 6+offset_days)
relative_path = '' # This isn't relevant anymore with reorganization of code, but still needs to be empty string



# TCG scraping variables
URL = "https://www.tcgplayer.com/product/242811/pokemon-celebrations-celebrations-elite-trainer-box?Language=English" # The URL for the webpage to pull from



# Twitter scraping Variables
tags = ['Pokemon', 'Celebrations']
limitItems = False # If this is true, then the maximum amount of items pulled is maximumItems
maximumItems = 10
trackingPopularityPerTweet = False # Take each tweet and add its likes, retweets, and replies as an additional "hit" for that day
use_followers = False # Use follower count of twitter users
# likeretweetreply also needs to be set if you want to acquire those variables. It also plays a factor in processing, so it is listed there.


# Price variables
NUMBER_OF_LINES = 21324 # MANUAL: Update this value. This number needs to manually be updated to match how many lines your extension file has for price data (usually etb.txt)
date_price_bool = False # If this is true, then when running process.py it generates a graph comparing date to price. 
date_quantity_bool = False # If True, it generates date to quantity sold. Cannot be true when date_price is true
correlation_generate = True # USED FOR BOTH TWITTER AND PRICE DATA. If True, finds the correlation



#Twitter processing variables. T
filter = True # if filter is on, then remove all tweets before october
# num_tweets = 17838//2 # The number of tweets we're going through (number of lines divided by 2 floored, since each tweet is two lines)

num_tweets = 44530//5 # MANUAL: Update this value. This is the latest for like and reply data. Must be the number of lines // 5 (5 lines per piece of data)
twitter_graphing_extension='tweet_likeretweetreply.txt' # Needs to be updated whenever we change the extension

# num_tweets = 17808//2 # This is the latest values for tweet_data
# twitter_graphing_extension = 'tweet_data.txt'

# These impact graphing.py file and what it graphs
use_likes = False # Maximum of 1 out of these 4 can be true
use_retweets = False 
use_replies = False
use_sum = False
likeretweetreply = True # Writes the variables for building a model. Must be true if any of the 4 above are true




# Regression model variables
multiple_models = True # Show all the models: date, volume, date and volume, date volume likes retweets replies.
normalize_terms = True # Cannot normalize if using old days?
use_old_days = False # Use data from 7 to 14 days ago
num_of_shift_days = 7 # Constant variable
regression_model = 0 # 0 = Linear Regression, 1 = SGDRegressor, 2 = Elastic Net, 3 = Kernel Ridge, 4 = BayesianRidge



# Autocorr variables
show_autocorr = True # Show the autocorrelation plot
show_volume_lag = False # If True, shows a lag plot for volume. If False, shows a lag plot for price.

shift_days = 7 # No longer used?
persistence_autoregression_model = True # Generate autoregression model 
sliding_window = False # If true, varies the window size (history length) for AutoRegressive model
lag_correlation = True # Shows the lag plot correlation
price_file_extension = './tcg_scraper/etb.txt'