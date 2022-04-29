import numpy
import pandas as pd
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

if use_old_days:
    shifted = y.shift(7)    
    x = concat([shifted, x], axis=1)
    x = pd.DataFrame(x)
    x.columns = ["Old price", "Date", "Likes", "Retweets", "Replies", "Volume"]
    x = x.iloc[7:, :]
    y = y.iloc[7:]
    df = concat([x, y], axis=1)

    print("All using one week old price as well")
    
    

    # print(x)


if normalize_terms: # all the normalize_terms are normalizing the values
    x = preprocessing.normalize(x, norm='l2')
    x = pd.DataFrame(x)
    if not use_old_days:
        x.columns=["Date", "Likes", "Retweets", "Replies", "Volume"]
    else:
        x.columns = ["Old price", "Date", "Likes", "Retweets", "Replies", "Volume"]


# Using multiple different models with different input variables

def build_model(x_data, y_data):
    repetitions = 100
    sumscore = 0
    for i in range(repetitions):
        x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 7, shuffle=False)
        # LR = SGDRegressor(max_iter=10000)
        LR = LinearRegression()
        # LR = ElasticNet()
        # LR = KernelRidge()
        # LR = BayesianRidge()
        LR.fit(x_train, y_train)
        predict = LR.predict(x_test)
        # print(predict)
        # print("==========================================================\n\n\n\n\n=====================================")
        # print(y_test)
        sumscore += mean_squared_error(y_test, predict)
    return sumscore


print("Multiple Linear Regressions Models")
if normalize_terms:
    print("Features normalized")
else:
    print("Features not normalized")
repetitions = 100

sumscore = build_model(x, y)
print("Average score using likes, retweets, replies, volume, and date:")
print(sqrt(sumscore / repetitions))




if multiple_models:

    x = x.drop("Likes", axis=1)
    x = x.drop("Retweets", axis=1)
    x = x.drop("Replies", axis=1)

    sumscore = build_model(x, y)
    print("Average score using volume and date:")
    print(sqrt(sumscore / repetitions))

    x = x.drop("Volume", axis=1)


    sumscore = build_model(x, y)
    print("Average score using date:")
    print(sqrt(sumscore / repetitions))


    if normalize_terms:
        x = df.drop("Price", axis=1) # doesn't mutate df
        x = preprocessing.normalize(x, norm='l2')
        x = pd.DataFrame(x)
        if use_old_days:
            x.columns = ["Old price", "Date", "Likes", "Retweets", "Replies", "Volume"]

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
    print(sqrt(sumscore / repetitions))
