"""
First attempt to scrape.

Web page link (to scrape):
 1. http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA
 2. http://sultan.pricecall.co.il/
 3. https://michaelio.co.il/c/%D7%99%D7%A8%D7%A7%D7%95%D7%AA

Helpfull sites:
1. https://www.dataquest.io/blog/web-scraping-tutorial-python/
2. https://www.youtube.com/watch?v=ng2o98k983k
3. https://www.udemy.com/course/web-scraping-python-bs/learn/lecture/13378628#overview

Trying to scrape couple of fruits/vegetables names and prices, into a Array.
"""

from datetime import datetime
import pyodbc
import pandas as pd
from ImportData import importData
import CompareData


def dictionary(prod):
    return {
        'מוצר': prod
    }


if __name__ == '__main__':

    # Server name
    server = "LAPTOP-VNSLHC31"
    # Data base name
    database = "BraudeProject"
    # Establish SQL server connection to insert data
    # Define our connection string
    connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                        SERVER=' + server + '; \
                                        DATABASE=' + database + ';\
                                        Trusted_Connection=yes;')
    # Create the connection cursor
    dataBaseCon = connect.cursor()

    resemblance = []
    query = "SELECT * FROM Updates"
    dataBaseCon.execute(query)
    for date in dataBaseCon:
        print("The last time you refreshed the sites was: " + date.Last_Update)
        print("would you like to refresh again?")
    answer = str(input("Press Y"))
    if answer == 'Y':
        importData(dataBaseCon)
        delete_query = "DELETE FROM Updates"
        dataBaseCon.execute(delete_query)
        dataBaseCon.commit()
        lastUpdate = datetime.now()
        insert_query = 'INSERT INTO Updates (Last_Update)' \
                       'VALUES (?);'
        dataBaseCon.execute(insert_query, lastUpdate.strftime("%d/%m/%Y %H:%M:%S"))
        dataBaseCon.commit()
        print("The last time you refreshed the sites was: " + lastUpdate.strftime("%d/%m/%Y %H:%M:%S"))
    else:

        # Analyze data
        resemblance = CompareData.compareData(dataBaseCon)
        select_query_UserProdInfo = "SELECT baseProd FROM [BraudeProject].[dbo].[UserProdInfo] WHERE siteName = " \
                                    "'Kishurit' "
        UserProdInfo_Sultan = []
        dataBaseCon.execute(select_query_UserProdInfo)
        for row in dataBaseCon:
            UserProdInfo_Sultan.append(row.baseProd)
        select_qurey_Sultan = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Kishurit'"
        dataBaseCon.execute(select_qurey_Sultan)
        sultan_Prods = []
        for row in dataBaseCon:
            sultan_Prods.append(row.Prod_Name)
        for baseProd in UserProdInfo_Sultan:
            print("המוצר "+ baseProd + " לא נמצא באתר סולטן ")
            print("האם התכוונת לאחד מהמוצרים הללו(במידה וכן יש לבחור את מס' המוצר):")
            df = pd.DataFrame.from_records([dictionary(l) for l in sultan_Prods])
            print(df)
            answer = int(input("בחר מס' אחרת הכנס 1-:"))
            if answer != -1:
                insert_query = 'INSERT INTO UserProdInfo (baseProd,userProdList,siteName)' \
                               'VALUES (?,?,?);'
                row = (baseProd, sultan_Prods[answer], "Kishurit")
                dataBaseCon.execute(insert_query, row)
                dataBaseCon.commit()
                sultan_Prods.remove(sultan_Prods[answer])

        # print(resemblance)
        # df = pd.DataFrame.from_records([dictionary(l) for l in resemblance])
        # print(df)




