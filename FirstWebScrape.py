"""
First attempt to scrape.

Web page link -> http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA

Helpfull sites:
1. https://www.dataquest.io/blog/web-scraping-tutorial-python/
2. https://www.youtube.com/watch?v=ng2o98k983k
3. https://www.udemy.com/course/web-scraping-python-bs/learn/lecture/13378628#overview

Trying to scrape couple of fruits/vegetables names and prices, into a Array.

"""
import inline as inline
import matplotlib as matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

pageCount = 3  #The number of pages in "משק כישורית" webpage.


"""
scrapePage - This method scrape a web page and extract the relevant data (price and name ) to a list.
Args: pageNumber -> the page number in this webpage.
"""

def scrapePage(pageNumber):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    r = requests.get(
        'http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page=' + str(pageNumber),
        headers=headers)  # , proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)

    Vegetables = []
    Prices = []

    for Element in soup.findAll('div',attrs={'class':'layout_list_item css_class_47954'}):
        Vegetables.append(Element.find('a').contents[0])
        Prices.append()


for i in range(1,pageCount+1):
    scrapePage(i)

#Vegetables = []
#Price = []

