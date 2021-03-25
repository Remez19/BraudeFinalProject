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
        self.progress = queue.Queue()
        selectFromDB(self.dataBaseCon, "SELECT * FROM Updates", self.progress)
        # Gui preparation

        self.mainWindow = tix.Tk()
        self.mainWindow.title('Braude Project')
        self.mainWindow.geometry('800x600')
        self.mainWindow.config(bg='black')

        self.WelcomeLabelFont = font.Font(family="Helvetica", size=15, weight=font.BOLD,
                                          underline=1)

        self.WelcomeLabel = Label(self.mainWindow, text="Hello Admin", font=self.WelcomeLabelFont)
        self.LastUpdateDateLabel = Label(self.mainWindow,
                                         text='The last time you updated the DB was: ' + self.progress.get()[0], fg="#FFBD09", bg='black')
        self.UpdateDbBtn = Button(self.mainWindow, text="Update Data Base",
                                  command=self.updateDataBaseBtn, width=20, height=1)
        self.mainWindow.update()
        self.EditDbBtn = Button(self.mainWindow, text="Edit data base ", command=self.EditDbBtn, width=20, height=1)
        # self.progressBar = ttk.Progressbar(self.mainWindow, orient=HORIZONTAL, length=100, mode='determinate')
        self.loadingLabel = Label(self.mainWindow, text="Loading...", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.LoadingBar = []
        for i in range(10):
            self.LoadingBar.append(Label(self.mainWindow, bg='#1F2732', width=1, height=1))

        # Tree View
        self.treeView = ttk.Treeview(self.mainWindow)
        self.treeView['columns'] = ('שם מוצר', 'יחידה', 'מחיר', 'אתר', 'מוצר בסיס')
        self.treeView.column('#0', width =0, minwidth=25)
        self.treeView.column('שם מוצר', anchor=S, width=15)
        self.treeView.column('יחידה', anchor=S, width=15)
        self.treeView.column('מחיר', anchor=S, width=15)
        self.treeView.column('אתר', anchor=S, width=15)
        self.treeView.column('מוצר בסיס', anchor=0, width=15)




        self.WelcomeLabel.place(x=370, y=10)
        self.LastUpdateDateLabel.place(x=270, y=50)
        self.UpdateDbBtn.place(x=350, y=78)
        self.EditDbBtn.place(x=350, y=110)
        # Gui preparation

    def printQ(self):
        print(list(self.progress.queue))

    def startApp(self):
        self.mainWindow.mainloop()


    def EditDbBtn(self):
        self.LastUpdateDateLabel.grid_forget()
        self.loadingLabel.place(x=350, y=73)
        self.UpdateDbBtn.place(x=350, y=145)
        self.EditDbBtn.place(x=350, y=185)
        self.progress.queue.clear()
        for i, label in enumerate(self.LoadingBar):
            label.place(x=(i + 15) * 22, y=100)
        self.UpdateDbBtn['state'] = 'disable'
        self.EditDbBtn['state'] = 'disable'
        self.thread = Thread(target=selectFromDB, args=(self.dataBaseCon, 'SELECT * FROM [BraudeProject].[dbo].['
                                                                          'AllProds]', self.progress))

        self.thread.start()
        self.loadingAnimation()

        # while
        # return



    def updateDataBaseOp(self):
        self.loadingAnimation()
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
        self.LastUpdateDateLabel.place(x=270, y=50)
        self.UpdateDbBtn.place(x=350, y=78)
        self.EditDbBtn.place(x=350, y=110)
        self.UpdateDbBtn['state'] = 'active'
        self.EditDbBtn['state'] = 'active'
        self.mainWindow.update()

    def updateDataBaseBtn(self):
        self.LastUpdateDateLabel.grid_forget()
        self.loadingLabel.place(x=350, y=73)
        self.UpdateDbBtn.place(x=350, y=145)
        self.EditDbBtn.place(x=350, y=185)
        # self.progressBar.place(x=250, y=100)
        for i, label in enumerate(self.LoadingBar):
            label.place(x=(i + 15) * 22, y=100)
        self.UpdateDbBtn['state'] = 'disable'
        self.EditDbBtn['state'] = 'disable'
        self.thread = Thread(target=importData, args=(self.dataBaseCon, self.progress, semProg))
        self.thread.start()
        self.mainWindow.after(100, self.updateDataBaseOp)

    def loadingAnimation(self):
        while self.thread.is_alive():
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
