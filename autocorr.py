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

date_price = find_averages_data(date_dict)[0]

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

df = pd.DataFrame(lrrprice)

df = df.loc[::-1].reset_index(drop=True) # need to put old dates at the start. Had to swap rows

df.columns = ["Date", "Likes", "Retweets", "Replies", "Volume", "Price"]

y = df.loc[:,"Price"]
x = df.drop("Price", axis=1) # doesn't mutate df

# Autocorrelation - Shows us the best amount of lag. Use y as it is price
if show_autocorr:
    # Used to show the autocorrelation plot, which is the correlation of lag plots but for every amount of day offset then graphed
    # autocorrelation_plot(y)

    # Lag plot
    lag_plot(y)
    shifted = concat([y.shift(7), y], axis=1)
    print(shifted.corr())
    print(y)

    plt.title("Lag Plot for Price Data")
    plt.show()



# Persistence model
def model_persistence(x):
    return x

if persistence_autoregression_model:

    for s in range(7, 36):
        shift_days = s
        sum_error = 0
        repetitions = 20

        for i in range(repetitions):

            window = shift_days # Used to determine how many days shift
            train, test = y[1:len(y) - 7 - i], y[len(y) - 7 - i: len(y) - i] # Split the data from the beginning to the different end points, defined by i

            model = AutoReg(train, lags=window) # lags is the number of days it remembers to use as "training"
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
                # This is used to print out predictions for a particular loop
                if i == 0 and s == 7: 
                    print('Predicted: ', yhat, "  Actual: " , obs)

            sum_error += sqrt(mean_squared_error(test_list, predictions))
        
        
        print('Test RMSE given ', s , 'days of info: ',  sum_error / repetitions)

