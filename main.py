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
from ImportData import importData
import CompareData

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
        print("The last time you refreshed the sites was: "+date.Last_Update)
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
        print(resemblance)
