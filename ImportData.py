from KishuritClass import Kishurit
from SultanClass import Sultan
from MichaeliClass import Michaeli
from Utils import deleteFromDB, selectFromDB
import threading
import time
from threading import Thread, Semaphore

sem = threading.Semaphore() # parallel computing -> using semaphore to sync threads

# Link to 'משק כישורית' site.
def importData(dataBaseCon):
    deleteBeforeInsert(dataBaseCon)
    # Devide to Threads
    Threads = []
    webObjList = []
    baseNames = selectFromDB(dataBaseCon, "SELECT * FROM [BraudeProject].[dbo].[AllVegNames]")
    kishurit = Kishurit(baseNames)
    sultan = Sultan(baseNames)
    # michaeli = Michaeli()
    # webObjList.append(michaeli)
    webObjList.append(kishurit)
    webObjList.append(sultan)
    for webObj in webObjList:
        Threads.append(Thread(target=webObj.startScrape, args=(sem, dataBaseCon)))
    startTime = time.time()
    for thread in Threads:
        thread.start()
    for thread in Threads:
        thread.join()
    endTime = time.time()
    print('#####  ' + str((endTime - startTime) / 60) + '  ####')



# Delete all the data from tables in order to update them

"""
:
"""
def deleteBeforeInsert(dataBaseCon):
    try:
        delete_query = "DELETE FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Sultan'"
        deleteFromDB(dataBaseCon, delete_query)
        delete_query = "DELETE FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Kishurit'"
        deleteFromDB(dataBaseCon, delete_query)
        delete_query = "DELETE FROM [BraudeProject].[dbo].[AllProds] WHERE Prod_Web = 'Michaeli'"
        deleteFromDB(dataBaseCon, delete_query)
        print("DB READY FOR INSERT")
    except Exception:
        print("Data Base delete FAILURE")
        exit(1)