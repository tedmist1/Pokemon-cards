import sys
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Basic scraper for tcgplayer. Need to fix some constant variables and make this more adaptable so I can gather data from other products. 
# Output data is just a text file with each data point taking up 4 lines. Needs to be handled in post-process to put into csv.

#USAGE: Run this file "scrape.py > file.txt" where file.txt is the name of the file you're writing to. You'll need to update process.py to include the name of your new file.

# IMPORTANT NOTE: It seems that tcgplayer only stores around the last 5125 sales, as each week when I update it, I get less of the old sales depending on how many new sales (even when adjusting my numbers for how many to look for)


# a linkt for the tcg page for the product you wish to scrape
URL = "https://www.tcgplayer.com/product/242811/pokemon-celebrations-celebrations-elite-trainer-box?Language=English"

# Finds the button to load more elements
def hit_load_button(num=100):
    for i in range(num): # Probably should change to be not 100 times but some varying amount of time
        try:
            load_more_button = browser.find_element(By.XPATH, "//*[@class='price-guide-modal__load-more']")
            load_more_button.click()
        except:
            break
        
        time.sleep(0.3)



# Launch web-driver
browser = webdriver.Firefox()
browser.get(URL)
time.sleep(3)
html = browser.page_source



# class tag to find the "view sales history" button
input = browser.find_element(By.XPATH, "//*[@class='svg-inline--fa fa-chevron-right']")
input.click()

# SUCCESS! able to open up data here
time.sleep(2)

hit_load_button(200) # Should eliminate this magic number and determine how to stop when fully done

output = browser.find_element(By.XPATH, "//*[@class='is-modal']")
print(output.text) # Needs to be fed into a file

browser.quit()


