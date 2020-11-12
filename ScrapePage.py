from bs4 import BeautifulSoup
import requests
from Vegetable import Vegetable

"""
scrapePageKishurit - This method scrape a web page and extract the relevant data (price and name ) to a list in 
"משק כישורית" website.
 """


def scrapePageKishurit(pageNumber, pageLink):
    """
    :rtype list of vegetables.
    :param pageNumber: the page number in this webpage.
    :param pageLink: the web page address
    :return Vegetables: all the vegetables products in this page.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    r = requests.get(
        pageLink + str(pageNumber),
        headers=headers)  # , proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content, features="html.parser")

    Vegetables = []
    for Element in soup.findAll('div', attrs={'class': 'layout_list_item css_class_47954'}):
        temp = Element.find('a').contents[0]
        index = temp.find('(')
        # retrieve the unit
        unit = temp[index:]
        unit = unit.replace("(", "")
        unit = unit.replace(")", "")
        # retrieve the name
        name = temp[:index]
        name = name.replace("כישורית", "")
        name = name.replace("*במבצע*", "")
        # retrieve the price
        price = Element.find('strong').contents[0]
        price = price.replace('₪', '')
        Vegetables.append(Vegetable(name, price, unit))

    return Vegetables


"""scrapePageSultan - This method scrape a web page and extract the relevant data (price and name ) to a list in 
"סולטן" website. """


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
        # retrieve price and delete duplicate spaces
        price = ElementPrice.contents[0]
        price = " ".join(price.split())
        Vegetables.append(Vegetable(name, price, unit))
    return Vegetables
