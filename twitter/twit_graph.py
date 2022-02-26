import math
import numpy as np
from scipy import stats
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates

filter = True # if filter is on, then remove all tweets before october
start_date = datetime(2021, 10, 24) # IDK why this has to be 23 and not 24. Need to revisit this.
end_date = datetime(2022, 2, 4)

# start_date = datetime(2021, 10, 23) # 2/14 there are 0 tweets. Need to fix it to have a '0' datapoint
# end_date = datetime(2022, 2, 21)



# start_date = datetime(2021, 10, 1)

num_tweets = 17838//2

# num_tweets = 10

# Assume data is given as dates \n username
# Going to be used to filter out users who are tweeting too much in a day
def collect_dates_user(relative_path='', extension='tweet_data.txt'):
    f = open(relative_path+extension, "r")

    date_users ={}
    for l in range(num_tweets):
        date = f.readline().strip()
        user = f.readline().strip()
        # print(user)
        loc = date.find(" ")
        date = date[2:loc] # chop off after the " " and the 20 in 2022/2021
        date_time_obj = datetime.strptime(date, '%y-%m-%d')



        if date_time_obj in date_users:
            if not user in date_users[date_time_obj]: # Dont add duplicates with the same user
                date_users[date_time_obj].append(user)
        else:
            date_users[date_time_obj] = [user] # keeping track of the users on particular dates


    # print(date_users)
    dates = {}
    for i in date_users:
        dates[i] = len(date_users[i])

    return dates




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
    dates = collect_dates_user()
    processed_data = process_data(dates)

    np_data = np.array(processed_data)
    build_raw_graph()

# data = np.genfromtxt('tweet_time.txt', skip_header=1, delimiter=';')
# date_time = data
# print(dates)
