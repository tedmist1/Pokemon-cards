import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
from selenium import webdriver






URL = "https://www.tcgplayer.com/product/242811/pokemon-celebrations-celebrations-elite-trainer-box?Language=English"

driver = webdriver.Firefox()
driver.get(URL)

html = driver.page_source
soup = BeautifulSoup(html, features="html.parser")

print(soup.prettify())

# page = requests.get(URL)

# print(page.text)