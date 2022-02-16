import math
import numpy as np
from scipy import stats
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates

#USAGE: Run this file after running scrape.py to generate a graph of the data.

# CONSTANTS

def read_from_file(number_of_lines, extension='etb.txt'):

    line_count = number_of_lines
    f = open(extension, "r")
    # problem: this reads all the lines. We dont want to read all the lines until we're ready.
    items = []
    date_dict = {} # a Dictionary to sort things by date
    for l in range(math.ceil(line_count/4)):
        date = f.readline().strip()
        status = f.readline().strip()
        count = f.readline().strip()
        price = f.readline().strip()
        price = price[1:] # Remove the $ signt
        items.append((date, status, count, price))

        # repeat multiple times if multiple sales
        for i in range(int(count)):
            # 
            if date in date_dict:
                date_dict[date].append(float(price))
            else: 
                date_dict[date] = [float(price)]
    f.close()
    return (items, date_dict)

def find_averages_data(date_dict):

    # Remove outliers and also find average prices
    date_price = []
    date_price_dict = {}
    for date in date_dict:
        z = np.abs(stats.zscore(date_dict[date]))
        outliers = np.where(z > 2) # Magic zscore number. Dont want quite 2 bc trying to filter items that are the wrong item. 

        # gross way to do it but keep track of how many removed so we remove the right ones
        total_removed = 0
        for i in outliers[0]:
            date_dict[date].pop(i-total_removed)
            total_removed+=1

        # If not enough sales happened that day throw it out
        if(len(date_dict[date]) < 10):
            continue

        date_time_obj = datetime.strptime(date, '%m/%d/%y')
        date_price.append([date_time_obj, np.mean(date_dict[date])])
        date_price_dict[date_time_obj] = np.mean(date_dict[date])
    return (date_price, date_price_dict)

def build_raw_graph():
    x = np_data[:,0]
    y = np_data[:,1]
    dates = matplotlib.dates.date2num(x)
    plt.plot_date(dates, y)
    plt.ylabel("Price")
    plt.title("Average price by day")
    plt.show()


if __name__ == "__main__":


    NUMBER_OF_LINES = 20100 # This  number needs to manually be updated ot match how many lines your extension file has

    items, date_dict = read_from_file(NUMBER_OF_LINES) 

    date_price, temp = find_averages_data(date_dict)[0]

    # Convert to np array


        
    np_data = np.array(date_price)
    print(np_data)
    build_raw_graph()