import numpy
import pandas as pd
import random
from twitter.twit_graph import *
from tcg_scraper.process import *
from myconfig import *
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, SGDRegressor, ElasticNet, BayesianRidge
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
from pandas import concat
from math import sqrt

# https://www.analyticsvidhya.com/blog/2021/05/multiple-linear-regression-using-python-and-scikit-learn/


'''
Linear Regression
from sklearn.linear_model import LinearRegression

Stochastic Gradient Descent Regression
from sklearn.linear_model import SGDRegressor

Kernel Ridge Regression
from sklearn.kernel_ridge import KernelRidge

Elastic Net Regression
from sklearn.linear_model import ElasticNet

Bayesian Ridge Regression
from sklearn.linear_model import BayesianRidge

LGBM Regressor
from lightgbm import LGBMRegressor

XGBoost Regressor
from xgboost.sklearn import XGBRegressor

CatBoost Regressor
from catboost import CatBoostRegressor



Gradient Boosting Regression
from sklearn.ensemble import GradientBoostingRegressor

Support Vector Machine
from sklearn.svm import SVR

'''



# TCG Data collection
items, date_dict = read_from_file(NUMBER_OF_LINES, './tcg_scraper/etb.txt')

# print(date_dict)
date_price = find_averages_data(date_dict)[0]
# print(date_price)

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

df = df.loc[::-1].reset_index(drop=True) # need to put old dates at the start. Had to swap rows

df.columns = ["Date", "Likes", "Retweets", "Replies", "Volume", "Price"]

# print(df)

y = df.loc[:,"Price"]
x = df.drop("Price", axis=1) # doesn't mutate df

lag_columns = ["Date", "Likes", "Retweets", "Replies", "Volume"]

if use_old_days:

    # NOTE: This was all backwards. This is predicting the future given many predictions in the future... Not useful!
    
    shifts = []
    for i in range(num_of_shift_days): # num_of_shift_days is the autocorr variable to determine how many days to shift by
        shift = y.shift(7+i)
        # print(shift[6:12]) 
        lag_columns = ["Old price" + str(i)] + lag_columns
        x = concat([shift, x], axis=1)
    x = pd.DataFrame(x)
    x.columns = lag_columns
    x = x.iloc[7+num_of_shift_days:, :] 
    y = y.iloc[7+num_of_shift_days:]
    df = concat([x, y], axis=1)
    print("All using price from 7 to 14 days ago as well")

    # shifts = []
    # for i in range(num_of_shift_days): # num_of_shift_days is the autocorr variable to determine how many days to shift by
    #     shift = y.shift(-7-i)
    #     # print(shift[6:12]) 
    #     lag_columns = ["Old price" + str(i)] + lag_columns
    #     x = concat([shift, x], axis=1)
    # x = pd.DataFrame(x)
    # x.columns = lag_columns
    # # print(x.iloc[:-5])
    # x = x.iloc[:-7-num_of_shift_days, :] 
    # y = y.iloc[:-7-num_of_shift_days]
    # df = concat([x, y], axis=1)
    # print("All using price from 7 to 14 days ago as well")

print(x)
print(y)

if normalize_terms: # all the normalize_terms are normalizing the values
    x = preprocessing.normalize(x, norm='l2')
    x = pd.DataFrame(x)
    if not use_old_days:
        x.columns=["Date", "Likes", "Retweets", "Replies", "Volume"]
    else:
        x.columns = lag_columns


# Using multiple different models with different input variables
repetitions = 20
def build_model(x_data, y_data):
    # repetitions = 1
    sumscore = 0
    prediction = []
    for i in range(repetitions):

        # For testing purposes, instead of just testing the last 7 days, check many different models where we test the last 7 days, test the 8th through 2nd to last days, test 9th through 3rd to last days, etc
        rand_end = i + num_of_shift_days # This allows us to test a variety of real data points. Chosen all from the end so we have data. Can't really use data points after our predictions because that's unfair
        len_x = len(x_data)

        x_test = x_data[len_x - rand_end:7 + len_x - rand_end]
        x_train = x_data[len_x - rand_end:]

        y_test = y_data[len_x - rand_end:7 + len_x - rand_end]
        y_train = y_data[len_x - rand_end:]
        LR = LinearRegression()
        # LR = SGDRegressor(max_iter=100000)
        # LR = ElasticNet()
        # LR = KernelRidge()
        # LR = BayesianRidge()
        LR.fit(x_train, y_train)
        predict = LR.predict(x_test)
        prediction = predict
        sumscore += sqrt(mean_squared_error(y_test, predict))
        if i == 0: # Print out actual vs prediction for the last 7 days
            print(y_test)
            print(prediction)

            
    return sumscore


print("Multiple Linear Regressions Models")
if normalize_terms:
    print("Features normalized")
else:
    print("Features not normalized")

sumscore = build_model(x, y)
print("Average score using likes, retweets, replies, volume, and date:")
print((sumscore / repetitions))




if multiple_models:

    x = x.drop("Likes", axis=1)
    x = x.drop("Retweets", axis=1)
    x = x.drop("Replies", axis=1)

    sumscore = build_model(x, y)
    print("Average score using volume and date:")
    print((sumscore / repetitions))

    x = x.drop("Volume", axis=1)


    sumscore = build_model(x, y)
    print("Average score using date:")
    print((sumscore / repetitions))


    if normalize_terms:
        x = df.drop("Price", axis=1) # doesn't mutate df
        x = preprocessing.normalize(x, norm='l2')
        x = pd.DataFrame(x)
        if use_old_days:
            x.columns = lag_columns

        else:
            x.columns=["Date", "Likes", "Retweets", "Replies", "Volume"]
        x = x.drop("Date", axis=1)
    else:
        x = df.drop("Date", axis=1)
        x = x.drop("Price", axis=1)  

    x = x.drop("Likes", axis=1)
    x = x.drop("Retweets", axis=1)
    x = x.drop("Replies", axis=1)


    sumscore = build_model(x, y)

    print("Average score using volume:")
    print(sumscore / repetitions)
