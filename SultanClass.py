from Utils import connectionChecker, insertToDB
from bs4 import BeautifulSoup
from VegetableClass import Vegetable
from Compare import compareNameToBaseName
import time

class Sultan:
    """
           A class used to represent the 'Sultan' Website

           ...

           Attributes
           ----------
           webName : str
               The name of the website = Sultan

           pageLink : str
               The page link of Kishurit website

           insertQuery : str
               The query to insert new vegetable to the DB

           resultVegList : list
               A list that contains all the vegetables in Kishurit website

           baseNameList : list
               A list that contains all the basic names of vegetables (retrieved from DATA BASE)
           Methods
           -------
           startScrape(self, sem, dataBaseCon)
               Starts scraping each page link in Sultan website.The start function of the threads

           getLinkData(self)
               Retrieve the link raw data of unit, price and name of a vegetable

           getVegDetails(self, title, price)
               Creates a Vegetable instance
    """

    def __init__(self, baseNameList, progress):
        """
               Parameters
               ----------
               baseNameList : list
                   A list of basic names of vegetable (retrieved from DATA BASE)
        """
        self.webName = 'Sultan'
        self.pageLink = 'http://sultan.pricecall.co.il/'
        self.insertQuery = 'INSERT INTO AllProds (Prod_Name,Prod_Unit,Prod_Price,Prod_Web,Base_Prod)' \
                           'VALUES (?,?,?,?,?);'
        self.resultVegList = []
        self.baseNameList = baseNameList
        self.progress = progress

    def startScrape(self, semDB, semProg, dataBaseCon):
        """Starts scraping each page link in Kishurit website.The start function of the threads.
               Parameters
               ----------
               sem : threading.Semaphore
                   Semaphore to synchronize the threads when inserting to DB

               dataBaseCon : pyodbc.connect.cursor
                   The connection to the DB
        """
        self.getLinkData()
        if len(self.resultVegList):
            step = 50 / len(self.resultVegList)
            semDB.acquire()
            for veg in self.resultVegList:
                row = veg.getRow()
                insertToDB(dataBaseCon, row, self.insertQuery)
                self.progress.put(step)
                semProg.acquire()
            print("Thread " + self.webName + " finish")
            semDB.release()

    def getLinkData(self):
        """Retrieve the link raw data of unit, price and name of a vegetable.
        """
        page = connectionChecker(self.pageLink, self.webName)
        html = BeautifulSoup(page.content, features="html.parser")
        for tableNumber, table in enumerate(html.findAll('tbody', attrs={'class': 'table-img-max-height'}), start=1):
            if tableNumber <= 3:
                for tr in table.find_all('tr'):
                    name = tr.find('td', attrs={'class': 'col-name'}).text
                    price = tr.find('td', attrs={'class': 'col-price'}).text
                    self.resultVegList.append(self.getVegDetails(name, price))

    def getVegDetails(self, name, price):
        """Creates a Vegetable instance
                       Parameters
                       ----------
                       name : str
                           Name and unit of vegetable

                       price : str
                           The price of the vegetable
                       """
        name = name.split()
        name = ' '.join(name)
        price = price.split()
        price = ' '.join(price)
        baseName = compareNameToBaseName(name, self.baseNameList)
        return Vegetable(name, price, 'ק"ג', self.webName, baseName)
