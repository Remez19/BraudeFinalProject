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

        self.xChange = 800
        self.yChange = 600
        self.treeViewFlag = False
        self.mainWindow = tix.Tk()
        self.mainWindow.title('Braude Project')
        self.mainWindow.geometry(f'{self.xChange}x{self.yChange}')
        self.mainWindow.config(bg='black')

        self.WelcomeLabelFont = font.Font(family="Helvetica", size=15, weight=font.BOLD,
                                          underline=1)
        # Labels
        self.WelcomeLabel = Label(self.mainWindow, text="Hello Admin", font=self.WelcomeLabelFont, fg='blue')
        self.LastUpdateDateLabel = Label(self.mainWindow,
                                         text='The last time you updated the DB was: ' + self.progress.get()[0],
                                         fg="#FFBD09", bg='black')
        self.loadingLabel = Label(self.mainWindow, text="Loading...", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.nameLabel = Label(self.mainWindow, text="מוצר שם", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.baseNameLabel = Label(self.mainWindow, text="בסיסי שם", font="Bahnschrift", bg='black', fg="#FFBD09")

        self.LoadingBar = []
        for i in range(10):
            self.LoadingBar.append(Label(self.mainWindow, bg='#1F2732', width=1, height=1))
        # Labels

        # Entry labels
        self.nameEntry = Entry(self.mainWindow, width=20)
        self.basicNameEntry = Entry(self.mainWindow, width=20)
        # Entry Labels

        # Buttons
        self.UpdateDbBtn = Button(self.mainWindow, text="Update Data Base",
                                  command=self.updateDataBaseBtn, width=20, height=1)
        self.EditDbBtn = Button(self.mainWindow, text="Edit data base", command=self.EditDbBtn, width=20, height=1)
        self.saveChangesBtn = Button(self.mainWindow, text="Save changes", command=self.EditDbBtn, width=20, height=1)
        # Buttons

        # self.progressBar = ttk.Progressbar(self.mainWindow, orient=HORIZONTAL, length=100, mode='determinate')

        # Tree View
        self.treeView = ttk.Treeview(self.mainWindow)
        self.treeView['columns'] = ('Prod_Name', 'Prod_Unit', 'Prod_Price', 'Prod_Web', 'Base_Prod')
        self.treeView.column('#0', anchor=S, width=0, minwidth=0)
        self.treeView.column('Prod_Name', anchor=S, width=90, minwidth=80)
        self.treeView.column('Prod_Unit', anchor=S, width=90, minwidth=80)
        self.treeView.column('Prod_Price', anchor=S, width=90, minwidth=80)
        self.treeView.column('Prod_Web', anchor=S, width=90, minwidth=80)
        self.treeView.column('Base_Prod', anchor=S, width=90, minwidth=80)

        self.treeView.heading('#0', text='', anchor=W)
        self.treeView.heading('Base_Prod', text='מוצר בסיס', anchor=S)
        self.treeView.heading('Prod_Name', text='שם מוצר', anchor=S)
        self.treeView.heading('Prod_Unit', text='יחידה', anchor=S)
        self.treeView.heading('Prod_Price', text='מחיר', anchor=S)
        self.treeView.heading('Prod_Web', text='אתר', anchor=S)
        self.treeView.bind('<ButtonRelease-1>', self.getItemFromList)
        # Tree View



        self.WelcomeLabel.place(x=356, y=10)
        self.LastUpdateDateLabel.place(x=260, y=50)
        self.UpdateDbBtn.place(x=340, y=78)
        self.EditDbBtn.place(x=340, y=110)


        # Gui preparation

    def startApp(self):
        self.mainWindow.mainloop()

    def windowResize(self, e):
        return

    def getItemFromList(self, e):

        selectedItem = self.treeView.focus()
        selectedItem = self.treeView.item(selectedItem, 'values')
        if len(selectedItem) > 1:
            self.basicNameEntry.delete(0, END)
            self.basicNameEntry.insert(0, selectedItem[4])
            self.nameEntry.delete(0, END)
            self.nameEntry.insert(0, selectedItem[0])
            self.mainWindow.update()

    def EditDbBtn(self):
        self.treeViewFlag = True
        self.LastUpdateDateLabel.grid_forget()
        self.treeView.place_forget()
        self.nameLabel.place_forget()
        self.nameEntry.place_forget()
        self.nameEntry.delete(0, END)
        self.baseNameLabel.place_forget()
        self.basicNameEntry.place_forget()
        self.basicNameEntry.delete(0, END)
        for i in self.treeView.get_children():
            self.treeView.delete(i)
        self.loadingLabel.place(x=375, y=73)
        self.UpdateDbBtn.place(x=350, y=145)
        self.EditDbBtn.place(x=350, y=185)
        self.progress.queue.clear()
        for i, label in enumerate(self.LoadingBar):
            label.place(x=(i + 15) * 21, y=100)
        self.UpdateDbBtn['state'] = 'disable'
        self.EditDbBtn['state'] = 'disable'
        self.thread = Thread(target=selectFromDB, args=(self.dataBaseCon, 'SELECT * FROM [BraudeProject].[dbo].['
                                                                          'AllProds]', self.progress))
        self.thread.start()
        self.loadingAnimation()
        self.loadingLabel.place_forget()
        for label in self.LoadingBar:
            label.place_forget()
        self.LastUpdateDateLabel.place(x=270, y=50)
        self.UpdateDbBtn.place(x=340, y=78)
        self.EditDbBtn.place(x=340, y=110)
        self.UpdateDbBtn['state'] = 'active'
        self.EditDbBtn['state'] = 'active'
        self.saveChangesBtn.place(x=340, y=480)
        self.nameLabel.place(x=560, y=390)
        self.nameEntry.place(x=497, y=420)
        self.baseNameLabel.place(x=400, y=390)
        self.basicNameEntry.place(x=342, y=420)
        self.treeView.place(x=220, y=150)
        i = 0
        while not self.progress.empty():
            self.treeView.insert(parent='', index='end', iid=i, values=tuple(self.progress.get()))
            i = i + 1

        self.mainWindow.update()

        # while
        # return

    def updateDataBaseOp(self):
        self.progress.queue.clear()
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
        self.UpdateDbBtn.place(x=340, y=78)
        self.EditDbBtn.place(x=340, y=110)
        if self.treeViewFlag:
            self.nameLabel.place(x=560, y=390)
            self.nameEntry.place(x=497, y=420)
            self.baseNameLabel.place(x=400, y=390)
            self.basicNameEntry.place(x=342, y=420)
            self.treeView.place(x=220, y=150)
        self.UpdateDbBtn['state'] = 'active'
        self.EditDbBtn['state'] = 'active'
        self.mainWindow.update()

    def updateDataBaseBtn(self):
        self.treeView.place_forget()
        self.nameLabel.place_forget()
        self.nameEntry.place_forget()
        self.nameEntry.delete(0, END)
        self.baseNameLabel.place_forget()
        self.basicNameEntry.place_forget()
        self.basicNameEntry.delete(0, END)
        self.LastUpdateDateLabel.grid_forget()
        self.loadingLabel.place(x=375, y=73)
        self.UpdateDbBtn.place(x=340, y=145)
        self.EditDbBtn.place(x=340, y=185)
        # self.progressBar.place(x=250, y=100)
        for i, label in enumerate(self.LoadingBar):
            label.place(x=(i + 15) * 21, y=100)
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
