"""
First attempt to scrape.

Web page link -> http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA

Helpfull sites:
1. https://www.dataquest.io/blog/web-scraping-tutorial-python/
2. https://www.youtube.com/watch?v=ng2o98k983k
3. https://www.udemy.com/course/web-scraping-python-bs/learn/lecture/13378628#overview

Trying to scrape couple of fruits/vegetables names and prices, into a Array.
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
from Vegetable import Vegetable

pageCount = 3  # The number of pages in "משק כישורית" webpage.
Vegetables = []  # All the vegetables from "משק כישורית" webpage.
Data = []  # One list of all the vegetables

"""
scrapePage - This method scrape a web page and extract the relevant data (price and name ) to a list.
"""


def scrapePage(pageNumber):
    """
    :rtype list of vegetables.
    :param pageNumber: the page number in this webpage.
    :return Vegetables: all the vegetables products in this page.
    """
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
    for Element in soup.findAll('div', attrs={'class': 'layout_list_item css_class_47954'}):
        temp = Element.find('a').contents[0]
        index = temp.find('(')
        # retrieve the unit
        unit = temp[index:]
        # retrieve the name
        name = temp[:index]
        # retrieve the price
        price = Element.find('strong').contents[0]
        price = price.replace('₪', '')
        Vegetables.append(Vegetable(name, price, unit))

    return Vegetables

    # Vegetables.append(Element.find('a').contents[0])


for i in range(1, pageCount + 1):
    Vegetables.append(scrapePage(i))

# falttern the data to single list
Data = [item for sublist in Vegetables for item in sublist]
# convert the data to a table
df = pd.DataFrame.from_records([d.to_dist() for d in Data])
# create a cvs file out of the table
df.to_csv('משק כישורית.csv', index=False, encoding='utf-8')
df = pd.read_csv("משק כישורית.csv")
temp = pd.ExcelWriter('משק כישורית.xlsx')
# create a excel flie from cvs
df.to_excel(temp, index=False)
temp.save()
