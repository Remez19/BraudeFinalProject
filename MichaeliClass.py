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



























#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# based on <https://stackoverflow.com/a/47920128/4865723>

from tkinter import *
import asyncio
import threading
import random
import queue


class AsyncioThread(threading.Thread):
    def __init__(self, the_queue, max_data):
        self.asyncio_loop = asyncio.get_event_loop()
        self.the_queue = the_queue
        self.max_data = max_data
        threading.Thread.__init__(self)

    def run(self):
        self.asyncio_loop.run_until_complete(self.do_data())

    async def do_data(self):
        """ Creating and starting 'maxData' asyncio-tasks. """
        tasks = [
            self.create_dummy_data(key)
            for key in range(self.max_data)
        ]
        await asyncio.wait(tasks)

    async def create_dummy_data(self, key):
        """ Create data and store it in the queue. """
        sec = random.randint(1, 10)
        data = '{}:{}'.format(key, random.random())
        await asyncio.sleep(sec)

        self.the_queue.put((key, data))


class TheWindow:
    def __init__(self, max_data):
        # thread-safe data storage
        self.the_queue = queue.Queue()

        # the GUI main object
        self.root = Tk()

        # create the data variable
        self.data = []
        for key in range(max_data):
            self.data.append(StringVar())
            self.data[key].set('<default>')

        # Button to start the asyncio tasks
        Button(master=self.root,
               text='Start Asyncio Tasks',
               command=lambda: self.do_asyncio()).pack()
        # Frames to display data from the asyncio tasks
        for key in range(max_data):
            Label(master=self.root, textvariable=self.data[key]).pack()
        # Button to check if the GUI is freezed
        Button(master=self.root,
               text='Freezed???',
               command=self.do_freezed).pack()

    def refresh_data(self):
        """
        """
        # do nothing if the aysyncio thread is dead
        # and no more data in the queue
        if not self.thread.is_alive() and self.the_queue.empty():
            return

        # refresh the GUI with new data from the queue
        while not self.the_queue.empty():
            key, data = self.the_queue.get()
            self.data[key].set(data)

        print('RefreshData...')

        #  timer to refresh the gui with data from the asyncio thread
        self.root.after(1000, self.refresh_data)  # called only once!

    def do_freezed(self):
        """ Button-Event-Handler to see if a button on GUI works.
            The GOAL of this example is to make this button clickable
            while the other thread/asyncio-tasks are working. """
        print('Tkinter is reacting. Thread-ID: {}'
              .format(threading.get_ident()))

    def do_asyncio(self):
        """
            Button-Event-Handler starting the asyncio part in a separate
            thread.
        """
        # create Thread object
        self.thread = AsyncioThread(self.the_queue, len(self.data))

        #  timer to refresh the gui with data from the asyncio thread
        self.root.after(1000, self.refresh_data)  # called only once!

        # start the thread
        self.thread.start()


if __name__ == '__main__':
    window = TheWindow(10)
    window.root.mainloop()

