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
from ScrapePage import scrapePageSultan
from ScrapePage import scrapePageKishurit
import pandas as pd

if __name__ == '__main__':

    # Link to 'משק כישורית' site.
    KishuritLink = 'http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page='
    SultanLink = 'http://sultan.pricecall.co.il/'
    pageCount = 3  # The number of pages in "משק כישורית" webpage.

    Vegetables = []  # All the vegetables from "משק כישורית" webpage and "סולטן" webpage.
    Data = []  # One list of all the vegetables
    for pageIndex in range(1,pageCount + 1):
        Vegetables.append(scrapePageKishurit(pageIndex, KishuritLink))

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

    # Create a excel file for sultan site too
    Vegetables = scrapePageSultan(SultanLink)
    df = pd.DataFrame.from_records([v.to_dist() for v in Vegetables])
    df.to_csv('סולטן.csv', index=False, encoding='utf-8')
    df = pd.read_csv('סולטן.csv')
    temp = pd.ExcelWriter('סולטן.xlsx')
    df.to_excel(temp, index=False)
    temp.save()
