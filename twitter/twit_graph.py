import math
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates

import sys
# Importing general information
sys.path.append('../')
from myconfig import *


# num_tweets = 10

# Assume data is given as dates \n username
# Going to be used to filter out users who are tweeting too much in a day
def collect_dates_user(relative_path='', extension='tweet_data.txt'):
    f = open(relative_path+extension, "r")

    date_users ={}
    date_popularity = {}

    date_list = [end_date - timedelta(days=x) for x in range((end_date - start_date).days)]

    for i in date_list:
        if not likeretweetreply:
            date_popularity[i] = 0
        else:
            date_popularity[i] = np.array([0, 0, 0, 0]) #like, retweet, reply, tweet_volume

    for l in range(num_tweets):
        date = f.readline().strip()
        user = f.readline().strip()
        popularity = 3 # Default popularity is 3 just for tweeting (using the natural log)
        if trackingPopularityPerTweet or use_followers: # Popularity and followercount behave the same
            popularity = int(f.readline().strip()) + 3 # Add popularity to the base value of 3, if we care about tweet popularity

        if likeretweetreply:
            like = int(f.readline().strip())
            retweet = int(f.readline().strip())
            reply = int(f.readline().strip())

       

        # print(user)
        loc = date.find(" ")
        date = date[2:loc] # chop off after the " " and the 20 in 2022/2021

        date_time_obj = datetime.strptime(date, '%y-%m-%d')

        if date_time_obj >= end_date or date_time_obj <= start_date:
            continue
        

        
        # We're just using date_users to make sure we dont have broken bots that spam tweeted. 
        # All the important information is stored in date_popularity now
        if date_time_obj in date_users:
            if not user in date_users[date_time_obj]: # Dont add duplicates with the same user
                date_users[date_time_obj].append(user)

                # print(popularity)
                # print(math.floor(math.log(popularity)))
                if not likeretweetreply:
                    date_popularity[date_time_obj] += math.floor(math.log(popularity)) # Default popularity of a tweet is 3, and add more to it per retweet, like, reply / follower count
                else:
                    date_popularity[date_time_obj] += np.array([like, retweet, reply, 1])


        else:
            date_users[date_time_obj] = [user] # keeping track of the users on particular dates

            if not likeretweetreply:
                date_popularity[date_time_obj] += math.floor(math.log(popularity)) # Default popularity of a tweet is 3, and add more to it per retweet, like, reply / follower count
            else:
                date_popularity[date_time_obj] += np.array([like, retweet, reply, 1])

    # print(date_users)
    # dates = {}
    # for i in date_users:
    #     dates[i] = len(date_users[i])

    return date_popularity




def collect_dates(relative_path='', extension='tweet_time.txt'):
    
    f = open(relative_path+extension, "r")
    dates = {}

    for l in range(num_tweets): # number of tweets
        date = f.readline().strip()
        # loc = date.find("+")
        # date = date[2:loc] # chop off after the + and the 20 in 2022/2021
        # date_time_obj = datetime.strptime(date, '%y-%m-%d %H:%M:%S')

        loc = date.find(" ")
        date = date[2:loc] # chop off after the + and the 20 in 2022/2021
        date_time_obj = datetime.strptime(date, '%y-%m-%d')

        if date_time_obj in dates:
            dates[date_time_obj] += 1
        else:
            dates[date_time_obj] = 1

    return dates


def process_data(dates):

    processed_data = []
    for i in dates:
        if not filter or (i > start_date and i < end_date):
            processed_data.append([i, dates[i]])
    return processed_data


def process_data_lrr(dates):
    e = math.e
    processed_data = []
    for i in dates:
        if not filter or (i > start_date and i < end_date):
            # processed_data.append([i, dates[i][0], dates[i][1], dates[i][2], dates[i][3]])
            # processed_data.append([(i - start_date_process).days, dates[i][0], dates[i][1], dates[i][2], dates[i][3]]) # 1st column is days since started
            processed_data.append([(i - start_date_process).days, math.log(e + dates[i][0]), math.log(e + dates[i][1]), math.log(e +dates[i][2]), dates[i][3]]) # log of likes, retweets, replies
    return processed_data



def build_raw_graph():
    x = np_data[:,0]
    y = np_data[:,1]
    dates = matplotlib.dates.date2num(x)
    plt.plot_date(dates, y)
    plt.ylabel("Volume")
    plt.title("Tweet volume by day")
    plt.show()

def build_date_correlation_arr(np_data):
    new_arr = []
    for i in range(len(np_data)):
        diff = (np_data[i][0] - start_date_process).days
        new_arr.append([diff, np_data[i][1]])
    return new_arr


if __name__ == "__main__":
    dates = collect_dates_user('', twitter_graphing_extension)
    processed_data = process_data(dates)

    np_data = np.array(processed_data)

    if correlation_generate:
        corr_arr = build_date_correlation_arr(np_data)
        np_corr = np.array(corr_arr)
        print(np.corrcoef(np_corr[:,0].astype(float), np_corr[:,1].astype(float))) # Correlation between date and price
    
        build_raw_graph()


# data = np.genfromtxt('tweet_time.txt', skip_header=1, delimiter=';')
# date_time = data
# print(dates)
