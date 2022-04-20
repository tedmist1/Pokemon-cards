import matplotlib.pyplot as plt 
import numpy
import pandas as pd
from pandas import concat
from pandas.plotting import lag_plot, autocorrelation_plot
from twitter.twit_graph import *
from tcg_scraper.process import *
from myconfig import *
from matplotlib import pyplot as plt


# Followed this tutorial: https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/


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

X = np_tcg_data[:,1].astype(float)
y = np_twitter_data[:,1]#.astype(float)

# Plot a lag plot of the X and y data? Not sure how the lagplot works on two features. Probably meaningless
# print(np_tcg_data)
# print(np_twitter_data)

# plotty = pd.DataFrame(np.array([X, y]))
# lag_plot(plotty)
# plt.show()



# Lag of one day on price
xpose = pd.DataFrame(np.transpose(np.array([X]))) # Needs to stay uncommented for autocorrelation
# # print(xpose)
# values = pd.DataFrame(xpose.values)
# dataframe = concat([values.shift(1), values], axis=1)
# dataframe.columns = ['t-1', 't+1']
# result = dataframe.corr()
# print(result)


# Autocorrelation - Shows us the best amount of lag

autocorrelation_plot(xpose)
plt.show()

