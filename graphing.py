import matplotlib.pyplot as plt 
import numpy
from twitter.twit_graph import *
from tcg_scraper.process import *

from myconfig import *


# TCG Data collection
items, date_dict = read_from_file(NUMBER_OF_LINES, './tcg_scraper/etb.txt')

# print(date_dict)
date_price = find_averages_data(date_dict)[0]
# print(date_price_dict)

# Twitter Data Collection

dates = collect_dates_user('./twitter/', twitter_graphing_extension) # filters out repeat tweeters on the same day
processed_data = process_data(dates)
np_twitter_data = np.array(processed_data)


np_tcg_data = np.array(date_price)

print(np_twitter_data.shape)
print(np_tcg_data.shape)

# print(np_tcg_data[:,0])
# print(np_twitter_data[:,0])

# Why is it so hard to combine them
one_d = np.transpose(np.array([np_tcg_data[:,1]]))

# combined = np.hstack((np_twitter_data, one_d))

# print(combined)

# print(np_tcg_data[:,1])

# print(np_twitter_data[:,1])

print(np.corrcoef(np_tcg_data[:,1].astype(float), np_twitter_data[:,1].astype(float)))

plt.scatter(np_twitter_data[:,1].astype(float), np_tcg_data[:,1].astype(float))
plt.show()
plt.figure()