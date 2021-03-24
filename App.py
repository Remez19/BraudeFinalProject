import threading
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import tix
from datetime import datetime
from ImportData import importData
from threading import Thread
import time
import queue
from Utils import connectToDB, selectFromDB, deleteFromDB, insertToDB

semProg = threading.Semaphore(0)


class App:
    def __init__(self):
        self.dataBaseCon = connectToDB('LAPTOP-VNSLHC31', 'BraudeProject')
        self.lastUpdateDate = selectFromDB(self.dataBaseCon, "SELECT * FROM Updates")
        self.progress = queue.Queue()
        # Gui preparation

        self.mainWindow = tix.Tk()
        self.mainWindow.title('Braude Project')
        self.mainWindow.geometry('600x400')
        self.mainWindow.config(bg='black')

        self.WelcomeLabelFont = font.Font(family="Helvetica", size=15, weight=font.BOLD,
                                          underline=1)

        self.WelcomeLabel = Label(self.mainWindow, text="Hello Admin", font=self.WelcomeLabelFont)
        self.LastUpdateDateLabel = Label(self.mainWindow,
                                         text='The last time you updated the DB was: ' + self.lastUpdateDate[0], fg="#FFBD09", bg='black')
        self.UpdateDbBtn = Button(self.mainWindow, text="Update Data Base",
                                  command=self.updateDataBaseBtn)
        self.MatchNames = Button(self.mainWindow, text="Design data base ", command=self.printQ)
        self.progressBar = ttk.Progressbar(self.mainWindow, orient=HORIZONTAL, length=100, mode='determinate')
        self.loadingLabel = Label(self.mainWindow, text="Loading...", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.LoadingBar = []
        for i in range(10):
            self.LoadingBar.append(Label(self.mainWindow, bg='#1F2732', width=1, height=1))

        self.WelcomeLabel.place(x=250, y=10)
        self.LastUpdateDateLabel.place(x=160, y=50)
        self.UpdateDbBtn.place(x=250, y=145)
        self.MatchNames.place(x=250, y=185)
        # Gui preparation

    def printQ(self):
        print(list(self.progress.queue))

    def startApp(self):
        self.mainWindow.mainloop()

    def refreshProgressBar(self):
        while self.thread.is_alive():
            while not self.progress.empty():
                for label in self.LoadingBar:
                    label.config(bg="#FFBD09")
                    time.sleep(0.06)
                    self.mainWindow.update()
                    label.config(bg="#1F2732")
                if not self.thread.is_alive():
                    break
                # self.progressBar['value'] += self.progress.get()
                # self.mainWindow.update()
            if self.progress.empty():
                semProg.release()
        deleteFromDB(self.dataBaseCon, deleteQuery="DELETE FROM Updates")
        lastUpdate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insertToDB(self.dataBaseCon, data=lastUpdate, insertQuery='INSERT INTO Updates (Last_Update)' \
                                                                  'VALUES (?);')
        # self.progressBar['value'] = 0
        # self.progressBar.place_forget()
        self.loadingLabel.place_forget()
        for label in self.LoadingBar:
            label.place_forget()
        self.LastUpdateDateLabel['text'] = "Operation COMPLETE last update: " + lastUpdate
        self.LastUpdateDateLabel.place(x=160, y=50)
        self.UpdateDbBtn['state'] = 'active'
        self.mainWindow.update()

    def updateDataBaseBtn(self):
        self.LastUpdateDateLabel.grid_forget()
        self.loadingLabel.place(x=215, y=73)
        # self.progressBar.place(x=250, y=100)
        for i, label in enumerate(self.LoadingBar):
            label.place(x=(i + 12) * 18, y=100)
        self.UpdateDbBtn['state'] = 'disable'
        self.thread = Thread(target=importData, args=(self.dataBaseCon, self.progress, semProg))
        self.thread.start()
        self.mainWindow.after(100, self.refreshProgressBar)
