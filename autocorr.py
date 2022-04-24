import numpy
import pandas as pd
from twitter.twit_graph import *
from tcg_scraper.process import *
from myconfig import *
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from pandas import concat
from pandas import DataFrame
from pandas.plotting import lag_plot, autocorrelation_plot

from statsmodels.tsa.ar_model import AutoReg
from math import sqrt




# Followed this tutorial: https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/


# TCG Data collection
items, date_dict = read_from_file(NUMBER_OF_LINES, './tcg_scraper/etb.txt')

# print(date_dict)
date_price = find_averages_data(date_dict)[0]
# print(date_price_dict)

# Twitter Data Collection

dates = collect_dates_user('./twitter/', twitter_graphing_extension) # filters out repeat tweeters on the same day
processed_data = process_data_lrr(dates)
np_twitter_data = np.array(processed_data)
np_tcg_data = np.array(date_price)

# Manipulation to make it a 2d array with one column
prices = []
for line in np_tcg_data[:,1]:
    prices.append([line])

# date like retween reply price 
lrrprice = numpy.append(np_twitter_data, prices, axis=1)
# print(lrrprice)

df = pd.DataFrame(lrrprice)
df.columns = ["Date", "Likes", "Retweets", "Replies", "Volume", "Price"]


y = df.loc[:,"Price"]
x = df.drop("Price", axis=1) # doesn't mutate df


# Autocorrelation - Shows us the best amount of lag. Use y as it is price
if show_autocorr:
    autocorrelation_plot(y)
    lag_plot(y)
    plt.show()



# Persistence model
def model_persistence(x):
    return x

if persistence_model:
    window = 30 # not sure exactly what window is meant to help with    
    train, test = y[1:len(y) - shift_days], y[len(y) - shift_days:] # using y bc y is price and we are just doing date/price

    model = AutoReg(train, lags=30) # lags is the number of days it remembers to use as "training"
    model_fit = model.fit()

    coef = model_fit.params

    # walk forward over time steps in test
    history = train[len(train) - window:]
    
    history_list = history.tolist()
    test_list = test.tolist()

    predictions = list()
    for t in range(len(test_list)):
        length = len(history_list)
        lag = [history_list[i] for i in range(length-window, length)]
        yhat = coef[0]
        for d in range(window):
            yhat += coef[d+1] * lag[window - d - 1]

        obs = test_list[t]
        predictions.append(yhat)
        history_list.append(obs)
        print('Predicted: ', yhat, "  Expected: " , obs)

    rmse = sqrt(mean_squared_error(test_list, predictions))
    
    print('Test RMSE: ',  rmse)

