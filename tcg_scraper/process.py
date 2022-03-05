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


#USAGE: Run this file after running scrape.py to generate a graph of the data.


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
        if(len(date_dict[date]) < 3):
            continue

        date_time_obj = datetime.strptime(date, '%m/%d/%y')

        if date_time_obj >= end_date_process or date_time_obj <= start_date_process:
            continue

        date_price.append([date_time_obj, np.mean(date_dict[date])])
        date_price_dict[date_time_obj] = np.mean(date_dict[date])
    return (date_price, date_price_dict)

def find_num_sales_date(date_dict):
    num_sales_date = []
    for date in date_dict:
        date_time_obj = datetime.strptime(date, '%m/%d/%y')

        num_sales_date.append([date_time_obj, len(date_dict[date])])
    return num_sales_date

def build_raw_graph():
    x = np_data[:,0]
    y = np_data[:,1]
    dates = matplotlib.dates.date2num(x)
    plt.plot_date(dates, y)
    plt.ylabel("Price")
    plt.title("Average price by day")
    plt.show()

def build_date_correlation_arr(np_data):
    new_arr = []
    for i in range(len(np_data)):
        diff = (np_data[i][0] - start_date_process)
        print(diff)
        new_arr[i] = [start_date_process - np_data[i][0], np_data[i][1]]
    return new_arr

if __name__ == "__main__":

    items, date_dict = read_from_file(NUMBER_OF_LINES) 

    date_price, temp = find_averages_data(date_dict)

    # Convert to np array


    # Generates a date-price graph
    if date_price:
        np_data = np.array(date_price)
        print(np_data)
        build_raw_graph()
    if date_quantity:
    # Generates a date-quantity graph
        daily_sales_dict = find_num_sales_date(date_dict)
        np_data = np.array(daily_sales_dict)
        print(np_data)
        build_raw_graph()

    # Generate correlation
    if correlation_generate:
        corr_arr = build_date_correlation_arr(np_data)
        prin(corr_arr)

    # print(np.corrcoef(np_tcg_data[:,1].astype(float), np_twitter_data[:,1].astype(float)))
