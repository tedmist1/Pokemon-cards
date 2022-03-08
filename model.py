import numpy
import pandas as pd
from twitter.twit_graph import *
from tcg_scraper.process import *
from myconfig import *
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# https://www.analyticsvidhya.com/blog/2021/05/multiple-linear-regression-using-python-and-scikit-learn/


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

# x = x.drop("Likes", axis=1)
# x = x.drop("Retweets", axis=1)
# x = x.drop("Replies", axis=1)
# x = x.drop("Volume", axis=1)
# x = x.drop("Date", axis=1)
# print(x)
print("Multiple Linear Regression Models")
repetitions = 1000
sumscore = 0
for i in range(repetitions):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
    LR = LinearRegression()
    LR.fit(x_train, y_train)
    sumscore += (LR.score(x_test, y_test))
print("Average score using likes, retweets, replies, volume, and date:")
print(sumscore / repetitions)

x = x.drop("Likes", axis=1)
x = x.drop("Retweets", axis=1)
x = x.drop("Replies", axis=1)

sumscore = 0
for i in range(repetitions):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
    LR = LinearRegression()
    LR.fit(x_train, y_train)
    sumscore += (LR.score(x_test, y_test))
print("Average score using volume and date:")
print(sumscore / repetitions)


x = x.drop("Volume", axis=1)
sumscore = 0
for i in range(repetitions):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
    LR = LinearRegression()
    LR.fit(x_train, y_train)
    sumscore += (LR.score(x_test, y_test))
print("Average score using date:")
print(sumscore / repetitions)

x = df.drop("Date", axis=1)
x = x.drop("Likes", axis=1)
x = x.drop("Retweets", axis=1)
x = x.drop("Replies", axis=1)
x = x.drop("Price", axis=1) 
sumscore = 0
for i in range(repetitions):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
    LR = LinearRegression()
    LR.fit(x_train, y_train)
    sumscore += (LR.score(x_test, y_test))
print("Average score using volume:")
print(sumscore / repetitions)
