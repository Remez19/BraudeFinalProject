from datetime import datetime
from ImportData import importData
from Utils import connectToDB, selectFromDB, deleteFromDB, insertToDB
from tkinter import *
from tkinter import font
from tkinter import tix
from App import App

if __name__ == '__main__':
    # GUI section #
    app = App()
    app.startApp()

