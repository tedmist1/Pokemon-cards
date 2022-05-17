# PokePricePredictor

- Project by Tyler Edmiston

PokePricePredictor is a Data Science and Machine Learning project. It pulls data from TCGplayer and Twitter, and uses the data to predict the price of the Pokemon Celebrations Elite Trainer Boxes (can easily be changed to other products from TCGplayer). 


## Installation
1. Clone the repository to a local folder.
2. Install Python 3 if it is not already installed.
3. Install the required Python libraries (selenium, pandas, matplotlib, sklearn, and statsmodels).


# myconfig.py

The file myconfig.py contains all the specifications for the project. In the file, each variable is detailed. A brief description is provided here for the different sections of variables.

1.  General variables. These are the variables used for both scraping and processing. Most of these have to do with the dates being used.
2. TCG Scraping variables. Used for specifications for acquiring data from TCGplayer.
3. Twitter scraping variables. Used to specify variables for scraping Twitter. 
4. Price variables. Determines which variables to use and correlations to generate when running the process.py file. Process.py organizes scraped price data into price averages.
5. Twitter processing variables. Describes which variables are used for graphing and processing the Twitter data.
6. Regression model variables. When generating the regression models in model.py, determines the specifications.
7. Autocorr variables. Determines the autocorrelation and lag plot variables for the autocorr.py file.

# Usage Instructions

The first step to running the project is data collection. Collected data is already pushed to the repository, but you can collect data manually as well.

To collect the price data, in the tcg_scraper folder, run 'scrape.py > file.txt' where file.txt is the name of the file you're writing to. This project by default wrote to 'etb.txt' and also reads fromt he same file.

To collect the twitter data, in the twitter folder, similarly run 'sn_scrape.py > file.txt' where file.txt is the name of the file you're writing to. Depending on your specifications in myconfig.py, the file will change. The mainly used file is tweet_likeretweetreply.txt if the variable *likeretweetreply* is set to True.

To visualize the price data, change the "Price variables" to match what you would like to visualize, and then run "process.py" in the tcg_scraper folder. This will also generate correlation.

To visualize the Twitter data, change the correlation_generate variable, and run twit_graph.py in the twitter folder.

To generate the regression models, set the myconfig.py variables, and then run model.py in the master folder. 

To generate lag plots, run autocorr.py with the show_autocorr variable set to True in myconfig.py. The file autocorr.py will also generate the autoregression model if set to do so. It will predict the next seven days, and give the RMSE for that data.