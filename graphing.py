import matplotlib.pyplot as plt 
import numpy
import pandas as pd
from pandas import concat
from twitter.twit_graph import *
from tcg_scraper.process import *

from myconfig import *


# TCG Data collection
items, date_dict = read_from_file(NUMBER_OF_LINES, './tcg_scraper/etb.txt')

# print(date_dict)
date_price = find_averages_data(date_dict)[0]
# print(date_price)

# Twitter Data Collection

dates = collect_dates_user('./twitter/', twitter_graphing_extension) # filters out repeat tweeters on the same day

# print(dates)

processed_data = process_data(dates) # processed data is an array with date, volume OR date, [likes, retweet, reply, volume]
np_twitter_data = np.array(processed_data)
np_tcg_data = np.array(date_price)
title = "Volume vs Price" # graph title
if likeretweetreply:
    temp = []
    if use_sum:
        for i in processed_data:
            print(i)
            temp.append([i[0], i[1][0] + i[1][1] + i[1][2]])
        np_twitter_data = np.array(temp)
        title = "Sum of likes, retweets, replies vs Price"
    elif use_likes:
        for i in processed_data:
            temp.append([i[0], i[1][0]])
        np_twitter_data = np.array(temp)
        title = "Likes vs Price"
    elif use_retweets:
        for i in processed_data:
            temp.append([i[0], i[1][1]])
        np_twitter_data = np.array(temp)
        title = "Retweets vs Price"
    elif use_replies:
        for i in processed_data:
            temp.append([i[0], i[1][2]])
        np_twitter_data = np.array(temp)
        title = "Replies vs Price"
    else: # volume vs price
        for i in processed_data:
            temp.append([i[0], i[1][3]])
        np_twitter_data = np.array(temp)
        # title = "Replies vs Price"
    
    # print(np_twitter_data)
    # print(np_twitter_data[:,1])



# print(np_twitter_data.shape)
# print(np_tcg_data.shape)

# print(np_tcg_data[:,0])
# print(np_twitter_data[:,0])

# print(np_tcg_data[:,1])
# print(np_twitter_data[:,1])

# Why is it so hard to combine them
one_d = np.transpose(np.array([np_tcg_data[:,1]]))

# combined = np.hstack((np_twitter_data, one_d))

# print(combined)

# print(np_tcg_data[:,1])

# print(np_twitter_data[:,1])


if lag_correlation:
    df = pd.DataFrame(np_tcg_data)
    # df.columns = ['Date', 'Volume']
    # lag = concat([df.Date, df.Volume.shift(7)], axis=1)
    # lag = lag.dropna()
    # new_arr = []
    # for row in lag.Volume:
    #     print(row)
    # np_lag = lag.to_numpy()
    # # print(np_lag[:,1])

    np_tcg_data_trim = np_tcg_data[7:]
    np_twitter_data_trim = np_twitter_data[:-7]

    print(np_tcg_data_trim[:10])
    print(np_twitter_data_trim[:10])
    
    title = "Volume vs Price 7 days ago"

    print(np.corrcoef(np_tcg_data_trim[:,1].astype(float), np_twitter_data_trim[:,1].astype(float)))
else:
    print(np.corrcoef(np_tcg_data[:,1].astype(float), np_twitter_data[:,1].astype(float)))




plt.scatter(np_twitter_data[:,1].astype(float), np_tcg_data[:,1].astype(float))
plt.xlabel("Tweet Volume")
plt.ylabel("Price")
plt.title(title)

plt.show()
plt.figure()