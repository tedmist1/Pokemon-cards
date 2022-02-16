import math
import numpy as np
from scipy import stats
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates

filter = True # if filter is on, then remove all tweets before october
start_date = datetime(2021, 10, 24)
# start_date = datetime(2021, 10, 1)




def collect_dates(relative_path='', extension='tweet_time.txt'):
    
    f = open(extension, "r")
    dates = {}
    for l in range(8843): # number of tweets
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
        if not filter or i > start_date:
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
    dates = collect_dates()
    processed_data = process_data()

    np_data = np.array(processed_data)
    build_raw_graph()

# data = np.genfromtxt('tweet_time.txt', skip_header=1, delimiter=';')
# date_time = data
# print(dates)
