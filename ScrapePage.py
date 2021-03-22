from bs4 import BeautifulSoup
import requests
import re
from Vegetable import Vegetable



def scrapePageSultan(pageLink):
    """
      :rtype list of vegetables.
      :param pageLink: the web page address
      :return Vegetables: all the vegetables products in this page.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    r = requests.get(pageLink, headers=headers)  # , proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content, features="html.parser")
    Vegetables = []

    for Element, ElementPrice in zip(soup.findAll('td', attrs={'class': 'col-name'}),
                                     soup.findAll('td', attrs={'class': 'col-price'})):
        temp = Element.contents[0]
        # retrieve unit
        if 'קילו' in temp:
            index = temp.find('קילו')
        elif 'צרור' in temp:
            index = temp.find('צרור')
        elif 'יחידה' in temp:
            index = temp.find('יחידה')
        elif 'ליטר וחצי' in temp:
            index = temp.find('ליטר וחצי')
        else:
            index = -1
        if index == -1:
            unit = 'לא מצויין'
            # retrieve name and delete duplicate spaces
            name = " ".join(temp.split())
        else:
            unit = temp[index:]
            unit = " ".join(unit.split())
            # retrieve name
            name = temp[:index]
            name = " ".join(name.split())
            name = name.strip()
        # retrieve price and delete duplicate spaces
        price = ElementPrice.contents[0]
        price = " ".join(price.split())
        Vegetables.append(Vegetable(name, price, unit))
    return Vegetables


"""scrapePageSultan - This method scrape a web page and extract the relevant data (price and name ) to a list in 
"משק מיכאלי" website. """


def scrapePageMichaeli(pageLink):
    """
          :rtype list of vegetables.
          :param pageLink: the web page address
          :return Vegetables: all the vegetables products in this page.
        """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    r = requests.get(pageLink, headers=headers)  # , proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content, features="html.parser")
    Vegetables = []
    allPages = []
    for Tab in soup.findAll('a', attrs={'data-type': 'Category', }):
        allPages.append(Tab['href'])
    for link in range(3):
        r = requests.get(allPages[link], headers=headers)  # , proxies=proxies)
        content = r.content
        soup = BeautifulSoup(content, features="html.parser")
        for Element, ElementPrice in zip(soup.findAll('a', attrs={'class': 'cc-product-link-title'}),
                                         soup.findAll('h3', attrs={'class': 'price_new low-price text notranslate'})):
            str = Element.getText()
            indexUnit = re.search(r"\d", str)
            if indexUnit is not None:
                name = str[:indexUnit.start()]
                name = " ".join(name.split())
                name = name[:name.index("-")]
                name = name.strip()
                unit = str[indexUnit.start():]
                unit = " ".join(unit.split())
            else:
                name = str
                name = " ".join(name.split())
                unit = 'לא מצויין'
            price = ElementPrice.getText()
            price = price.replace('₪', '')
            price = " ".join(price.split())
            Vegetables.append(Vegetable(name, price, unit))
    return Vegetables
