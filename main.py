"""
First attempt to scrape.

Web page link:
 1. http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA
 2. http://sultan.pricecall.co.il/

Helpfull sites:
1. https://www.dataquest.io/blog/web-scraping-tutorial-python/
2. https://www.youtube.com/watch?v=ng2o98k983k
3. https://www.udemy.com/course/web-scraping-python-bs/learn/lecture/13378628#overview

Trying to scrape couple of fruits/vegetables names and prices, into a Array.
"""

import os,time
from ImportData import importData

if __name__ == '__main__':
    lastUpdate = time.ctime(os.path.getmtime('C:/Users/rdone/PycharmProjects/BraudeFinalProject/סולטן.xlsx'))  # not
    # constant can change from pc to pc
    print("The last time you refreshed the sites was: "+lastUpdate)
    print("would you like to refresh again?")
    answer = str(input("Press Y"))
    if answer == 'Y':
        importData()
        lastUpdate = time.ctime(os.path.getmtime(
            'C:/Users/rdone/PycharmProjects/BraudeFinalProject/סולטן.xlsx'))  # not constant can change from pc to pc
        print("The last time you refreshed the sites was: " + lastUpdate)
    else:
        # Analyze data
        x = 0





