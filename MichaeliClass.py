from Utils import connectionChecker
from bs4 import BeautifulSoup
from VegetableClass import Vegetable

class Michaeli:
    def __init__(self):
        self.webName = 'Michaeli'
        self.pageLink = 'https://webaccess-il.rexail.com/?s_jwe=eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..3jB5d9K7gfxYPUNpmb-NOw.Z_HMYC-pDNV0Hus6VX0JlcGSMR9RWq_GGtiebKp7doHEOZLTGN-N_N7l4LMeK3v07sfgKXpEtzfMcZ97exKDsEzNz5lbbnoGQvZiRDfdFhg.bD6GjyLFdibtBZrOT80mRQ#/store-products-shopping-non-customers'
        self.insertQuery = 'INSERT INTO AllProds (Prod_Name,Prod_Unit,Prod_Price,Prod_Web)' \
                           'VALUES (?,?,?,?);'
        self.resultVegList = []

    def startScrape(self, sem, dataBaseCon):
        self.getLinkData()
        if len(self.resultVegList):
            sem.acquire()
            for veg in self.resultVegList:
                row = veg.getRow()
                dataBaseCon.execute(self.insertQuery, row)
                dataBaseCon.commit()
            print("Thread " + self.webName + "finish")
            sem.release()

    def getLinkData(self):
        page = connectionChecker(self.pageLink, self.webName)
        html = BeautifulSoup(page.content, features="html.parser")
        temp = html.findAll('div', attrs={'class', 'container categories-container'})
        for tableNumber, table in enumerate(html.findAll('tbody', attrs={'class': 'table-img-max-height'}), start=1):
            if tableNumber <= 3:
                print(tableNumber)
                for tr in table.find_all('tr'):
                    name = tr.find('td', attrs={'class': 'col-name'}).text
                    price = tr.find('td', attrs={'class': 'col-price'}).text
                    self.resultVegList.append(self.getVegDetails(name, price))


    def getVegDetails(self, name, price):
        name = name.split()
        name = ' '.join(name)
        price = price.split()
        price = ' '.join(price)
        return Vegetable(name, price, unit='ק"ג')


