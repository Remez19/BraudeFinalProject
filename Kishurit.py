import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re
from Vegetable import Vegetable

"""
:rtype list of vegetables.
:param pageNumber: the page number in this webpage.
:param pageLink: the web page address
:return Vegetables: all the vegetables products in this page.
"""


class Kishurit:
    def __init__(self, pageCount=3):
        self.webName = 'Kishurit'
        self.pageLink = 'http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page='
        self.insertQuery = 'INSERT INTO AllProds (Prod_Name,Prod_Unit,Prod_Price,Prod_Web)' \
                   'VALUES (?,?,?,?);'
        self.pageCount = pageCount
        self.linkList = []
        self.resultVegList = []
        self.createPagesLinks()

    """
     :rtype list of vegetables.
     :param pageNumber: the page number in this webpage.
     :param pageLink: the web page address
     :return Vegetables: all the vegetables products in this page.
     """

    def startScrape(self):
        for link in self.linkList:
            self.getLinkData(link)

    def getLinkData(self, link):
        page = self.connectionChecker(link)
        html = BeautifulSoup(page.content, features="html.parser")
        for div in html.find_all('div', attrs={'class': 'grid'}):
            title = div.find('div', attrs={'class': 'list_item_title_with_brand'}).text
            price = div.find('a', attrs={'class': 'price'}).text
            self.resultVegList.append(self.getVegDetails(title, price))

    def getVegDetails(self, title, price):
        price = int(''.join(re.findall(r'\d+', price)))
        title = title.replace("*במבצע*", "")
        title = title.replace("*זוג במבצע*", "")  # לנסות להשתמש בביטוי רגולרי
        name = title[:title.find('(')]
        unit = title[title.find('(') + 1:title.find(')')]
        unit = self.unitSelector(unit)
        return Vegetable(name, price, unit)

    def unitSelector(self, unit):
        if unit.find('ק"ג') is not -1:
            return 'ק"ג'
        elif unit.find("יח") is not -1:
            indexNumber = re.search(r"\d", unit)  # 2 יחידות לדוגמא
            if indexNumber:
                return unit[indexNumber.start()] + ' ' + "יח'"
            else:
                return "יח'"
        else:
            return "יח'"


    def createPagesLinks(self):
        for i in range(self.pageCount):
            link = self.pageLink + str(i + 1)
            self.linkList.append(link)

    def connectionChecker(self, link):
        try:
            session = requests.Session()
            retry = Retry(connect=5, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session.get(link)
        except Exception:
            print("Connection Failure KISHURIT")
            return None
