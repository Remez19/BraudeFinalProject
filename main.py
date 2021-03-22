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


def connectToDB():
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
    return connect.cursor()



if __name__ == '__main__':
    dataBaseCon = connectToDB()
    resemblance = []
    query = "SELECT * FROM Updates"
    dataBaseCon.execute(query)
    for date in dataBaseCon:
        print("The last time you refreshed the sites was: " + date.Last_Update)
        print("would you like to refresh again?")
    answer = str(input("Press Y:"))
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
    # else:
    #
    #     # Analyze data
    #     resemblance = CompareData.compareData(dataBaseCon)
    #     print(resemblance)
    #
    #     #############################################################################
    #
    #     # כישורית
    #
    #     select_query_UserProdInfo = "SELECT baseProd FROM [BraudeProject].[dbo].[UserProdInfo] WHERE siteName = " \
    #                                 "'Kishurit' "
    #     UserProdInfo_Kishurit = []
    #     dataBaseCon.execute(select_query_UserProdInfo)
    #     for row in dataBaseCon:
    #         UserProdInfo_Kishurit.append(row.baseProd)
    #     select_qurey_Kishurit = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Kishurit'"
    #     dataBaseCon.execute(select_qurey_Kishurit)
    #     kishurit_Prods = []
    #     for row in dataBaseCon:
    #         kishurit_Prods.append(row.Prod_Name)
    #     for baseProd in UserProdInfo_Kishurit:
    #         print("המוצר " + baseProd + " לא נמצא באתר כישורית ")
    #         print("האם התכוונת לאחד מהמוצרים הללו(במידה וכן יש לבחור את מס' המוצר):")
    #         df = pd.DataFrame.from_records([dictionary(l) for l in kishurit_Prods])
    #         print(df)
    #         answer = str(input("בחר מס' אחרת הכנס כל תו אחר:"))
    #         kishurit = "'Kishurit'"
    #         if not answer.isalpha():
    #             temp = kishurit_Prods[int(answer)]
    #             if temp.find("'") != -1:
    #                 temp1 = temp[:temp.find("'")]
    #                 temp = temp1 + "'" + temp[temp.find("'"):]
    #                 tempStringProd = "'" + temp + "'"
    #             else:
    #                 tempStringProd = "'" + kishurit_Prods[int(answer)] + "'"
    #             if baseProd.find("'") != -1:
    #                 btemp1 = baseProd[:baseProd.find("'")]
    #                 btemp2 = btemp1 + "'" + baseProd[baseProd.find("'"):]
    #                 tempStringBase = "'" + btemp2 + "'"
    #             kishurit_Prods.remove(kishurit_Prods[int(answer)])
    #         else:
    #             tempStringProd = "'לא קיים'"
    #         tempStringBase = "'" + baseProd + "'"
    #         update_query = 'UPDATE UserProdInfo SET userProdList = ' + tempStringProd + ' WHERE siteName = ' + kishurit + ' AND baseProd = ' + tempStringBase + ';'
    #         print(update_query)
    #         dataBaseCon.execute(update_query)
    #         dataBaseCon.commit()
    #     ############################################################################
    #     # סולטן
    #
    #     select_query_UserProdInfo = "SELECT baseProd FROM [BraudeProject].[dbo].[UserProdInfo] WHERE siteName = " \
    #                                 "'Sultan' "
    #     UserProdInfo_Sultan = []
    #     dataBaseCon.execute(select_query_UserProdInfo)
    #     for row in dataBaseCon:
    #         UserProdInfo_Sultan.append(row.baseProd)
    #     select_qurey_Sultan = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Sultan'"
    #     dataBaseCon.execute(select_qurey_Sultan)
    #     sultan_Prods = []
    #     for row in dataBaseCon:
    #         sultan_Prods.append(row.Prod_Name)
    #     for baseProd in UserProdInfo_Sultan:
    #         print("המוצר " + baseProd + " לא נמצא באתר סולטן ")
    #         print("האם התכוונת לאחד מהמוצרים הללו(במידה וכן יש לבחור את מס' המוצר):")
    #         df = pd.DataFrame.from_records([dictionary(l) for l in sultan_Prods])
    #         print(df)
    #         answer = str(input("בחר מס' אחרת הכנס כל תו אחר:"))
    #         sultan = "'Sultan'"
    #         if not answer.isalpha():
    #             temp = sultan_Prods[int(answer)]
    #             if temp.find("'") != -1:
    #                 temp1 = temp[:temp.find("'")]
    #                 temp = temp1 + "'" + temp[temp.find("'"):]
    #                 tempStringProd = "'" + temp + "'"
    #             else:
    #                 tempStringProd = "'" + sultan_Prods[int(answer)] + "'"
    #             if baseProd.find("'") != -1:
    #                 btemp1 = baseProd[:baseProd.find("'")]
    #                 btemp2 = btemp1 + "'" + baseProd[baseProd.find("'"):]
    #                 tempStringBase = "'" + btemp2 + "'"
    #             sultan_Prods.remove(sultan_Prods[int(answer)])
    #         else:
    #             tempStringProd = "'לא קיים'"
    #         tempStringBase = "'" + baseProd + "'"
    #         update_query = 'UPDATE UserProdInfo SET userProdList = ' + tempStringProd + ' WHERE siteName = ' + sultan + ' AND baseProd = ' + tempStringBase + ';'
    #         dataBaseCon.execute(update_query)
    #         dataBaseCon.commit()
    #     ############################################################################
    #     # מיכאלי
    #
    #     select_query_UserProdInfo = "SELECT baseProd FROM [BraudeProject].[dbo].[UserProdInfo] WHERE siteName = " \
    #                                 "'Michaeli' "
    #     UserProdInfo_Michaeli = []
    #     dataBaseCon.execute(select_query_UserProdInfo)
    #     for row in dataBaseCon:
    #         UserProdInfo_Michaeli.append(row.baseProd)
    #     select_qurey_Michaeli = "SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Michaeli'"
    #     dataBaseCon.execute(select_qurey_Michaeli)
    #     michaeli_Prods = []
    #     for row in dataBaseCon:
    #         michaeli_Prods.append(row.Prod_Name)
    #     for baseProd in UserProdInfo_Michaeli:
    #         print("המוצר " + baseProd + " לא נמצא באתר מיכאלי ")
    #         print("האם התכוונת לאחד מהמוצרים הללו(במידה וכן יש לבחור את מס' המוצר):")
    #         df = pd.DataFrame.from_records([dictionary(l) for l in michaeli_Prods])
    #         print(df)
    #         answer = str(input("בחר מס' אחרת הכנס כל תו אחר:"))
    #         michaeli = "'Michaeli'"
    #         if not answer.isalpha():
    #             temp = michaeli_Prods[int(answer)]
    #             if temp.find("'") != -1:
    #                 temp1 = temp[:temp.find("'")]
    #                 temp = temp1 + "'" + temp[temp.find("'"):]
    #                 tempStringProd = "'" + temp + "'"
    #             else:
    #                 tempStringProd = "'" + michaeli_Prods[int(answer)] + "'"
    #             if baseProd.find("'") != -1:
    #                 btemp1 = baseProd[:baseProd.find("'")]
    #                 btemp2 = btemp1 + "'" + baseProd[baseProd.find("'"):]
    #                 tempStringBase = "'" + btemp2 + "'"
    #             michaeli_Prods.remove(michaeli_Prods[int(answer)])
    #         else:
    #             tempStringProd = "'לא קיים'"
    #         tempStringBase = "'" + baseProd + "'"
    #         update_query = 'UPDATE UserProdInfo SET userProdList = ' + tempStringProd + ' WHERE siteName = ' + michaeli + ' AND baseProd = ' + tempStringBase + ';'
    #         dataBaseCon.execute(update_query)
    #         dataBaseCon.commit()
    #
    #     # print(resemblance)
    #     # df = pd.DataFrame.from_records([dictionary(l) for l in resemblance])
    #     # print(df)


