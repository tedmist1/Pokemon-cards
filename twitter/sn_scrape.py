import snscrape.modules.twitter as sntwitter
import pandas as pd

# Code very closely based on the tutorials linked below.
# https://betterprogramming.pub/how-to-scrape-tweets-with-snscrape-90124ed006af
# https://github.com/JustAnotherArchivist/snscrape/blob/master/snscrape/modules/twitter.py

# USAGE: Run sn_scrape.py > file.txt in order to save that data
# Hashtag is what you're searching for, and you can set limitItems to True, and give a maximum tweets you want to observe

import sys
sys.path.append('../')
from myconfig import *

# hashtag = ['#Celebrations', '#Pokemon'] # Finds those with #Pokemon AND #Celebrations


# Scrape twotter using the snscrape package
def collect_data():
    # List to append tweet data to
    tweets_list1= []

    # Goes through all the tweets with this data
    for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(hashtag).get_items()):
        
        if limitItems and i>maximumItems:
            break

        if trackingPopularityPerTweet or likeretweetreply:
            tweets_list1.append([tweet.date, tweet.hashtags, tweet.user, tweet.likeCount, tweet.retweetCount, tweet.replyCount])
        elif use_followers:
            tweets_list1.append([tweet.date, tweet.hashtags, tweet.user, tweet.user.followersCount])
        else:
            tweets_list1.append([tweet.date, tweet.hashtags, tweet.user])
        
        # tweets_list1.append([tweet.date, tweet.content, tweet.hashtags]) # removed content bc not using to filter
    return tweets_list1


tweets_list1 = collect_data()

if trackingPopularityPerTweet or likeretweetreply:
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'hashtags', 'User', 'Likes', 'Retweets', 'Replies'])
elif use_followers:
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'hashtags', 'User', 'Followers'])
else: 
    tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'hashtags', 'User'])

# Printing tweets.
for i in tweets_df1.index:
    print(tweets_df1['Datetime'][i])
    # print(tweets_df1['hashtags'][i])
    print(tweets_df1['User'][i])
    if trackingPopularityPerTweet:
        print(tweets_df1['Likes'][i] + tweets_df1['Retweets'][i] + tweets_df1['Replies'][i])
    elif use_followers:
            print(tweets_df1['Followers'][i])
    elif likeretweetreply:
        print(tweets_df1['Likes'][i]) 
        print(tweets_df1['Retweets'][i]) 
        print(tweets_df1['Replies'][i])
    
