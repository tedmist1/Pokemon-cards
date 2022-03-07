import math
import numpy as np
from scipy import stats
from datetime import datetime
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
    for l in range(num_tweets):
        date = f.readline().strip()
        user = f.readline().strip()
        popularity = 3 # Default popularity is 3 just for tweeting (using the natural log)
        if trackingPopularityPerTweet or use_followers: # Popularity and followercount behave the same
            popularity = int(f.readline().strip()) + 3 # Add popularity to the base value of 3, if we care about tweet popularity
        # print(user)
        loc = date.find(" ")
        date = date[2:loc] # chop off after the " " and the 20 in 2022/2021
        date_time_obj = datetime.strptime(date, '%y-%m-%d')


        
        # We're just using date_users to make sure we dont have broken bots that spam tweeted. 
        # All the important information is stored in date_popularity now
        if date_time_obj in date_users:
            if not user in date_users[date_time_obj]: # Dont add duplicates with the same user
                date_users[date_time_obj].append(user)

                # print(popularity)
                # print(math.floor(math.log(popularity)))
                date_popularity[date_time_obj] += math.floor(math.log(popularity)) # Default popularity of a tweet is 3, and add more to it per retweet, like, reply / follower count
        else:
            date_users[date_time_obj] = [user] # keeping track of the users on particular dates
            date_popularity[date_time_obj] = math.floor(math.log(popularity)) 


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



def build_raw_graph():
    x = np_data[:,0]
    y = np_data[:,1]
    dates = matplotlib.dates.date2num(x)
    plt.plot_date(dates, y)
    plt.ylabel("Volume")
    plt.title("Tweet volume by day")
    plt.show()


if __name__ == "__main__":
    dates = collect_dates_user('', twitter_graphing_extension)
    processed_data = process_data(dates)

    np_data = np.array(processed_data)
    build_raw_graph()

# data = np.genfromtxt('tweet_time.txt', skip_header=1, delimiter=';')
# date_time = data
# print(dates)
