import sys
import requests
import re
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# Basic scraper for tcgplayer. Need to fix some constant variables and make this more adaptable so I can gather data from other products. 
# Output data is just a text file with each data point taking up 4 lines. Needs to be handled in post-process to put into csv.



# Finds the button to load more elements
def scroll_down(num=1000):
    for i in range(num): # Probably should change to be not 100 times but some varying amount of time
        load_more_button = browser.find_element(By.XPATH, "//*[@class='price-guide-modal__load-more']")
        load_more_button.click()
        time.sleep(0.1 * num%10)



# Launch web-driver
URL = "https://twitter.com/search?q=%23Pokemoncelebrations&src=typd&f=live"
browser = webdriver.Firefox()
browser.get(URL)
time.sleep(0.5)
html = browser.page_source



# class tag to find the "view sales history" button
input = browser.find_element(By.PARTIAL_LINK_TEXT, "Pokemon")
input.send_keys(Keys.PAGE_DOWN)

input.send_keys(Keys.PAGE_DOWN)
input.send_keys(Keys.PAGE_DOWN)
input.send_keys(Keys.PAGE_DOWN)

# SUCCESS! able to open up data here

time.sleep(2)




browser.quit()


