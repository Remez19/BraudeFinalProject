import concurrent.futures
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import tix
from ImportData import importData, insertAdminData
import time

from Utils import connectToDB, selectFromDB, deleteFromDB, insertToDB


class App:
    def __init__(self):
        self.dataBaseCon = connectToDB('LAPTOP-VNSLHC31', 'BraudeProject')
        lastUpdate = selectFromDB(self.dataBaseCon, "SELECT * FROM Updates")
        self.baseNamesList = selectFromDB(self.dataBaseCon, 'SELECT * FROM [BraudeProject].[dbo].[AllVegNames]')
        self.baseNamesList = [''.join(item.split()) for sublist in self.baseNamesList for item in sublist]
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
                                         text='The last time you updated the DB was: ' + str(lastUpdate[0][0]),
                                         fg="#FFBD09", bg='black')
        self.loadingLabel = Label(self.mainWindow, text="Loading...", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.nameLabel = Label(self.mainWindow, text="מוצר שם", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.baseNameLabel = Label(self.mainWindow, text="בסיסי שם", font="Bahnschrift", bg='black', fg="#FFBD09")
        self.comboBoxLabel = Label(self.mainWindow, text="בסיס מוצרי", font="Bahnschrift", bg='black', fg="#FFBD09")

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
        self.saveChangesBtn = Button(self.mainWindow, text="Save changes", command=self.saveChangesBtn, width=20,
                                     height=1)
        self.saveItem = Button(self.mainWindow, text="Save", command=self.saveItemChangeToTable, width=10, height=1)
        # Buttons

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

        # ComboBox
        self.basicNameComBox = ttk.Combobox(self.mainWindow, width=15, textvariable=StringVar())
        self.basicNameComBox['values'] = tuple(self.baseNamesList)
        self.basicNameComBox['state'] = 'readonly'
        self.basicNameComBox.bind('<<ComboboxSelected>>', self.setBasicNameFromComboBox)
        # ComboBox

        self.WelcomeLabel.place(x=356, y=10)
        self.LastUpdateDateLabel.place(x=260, y=50)
        self.UpdateDbBtn.place(x=340, y=78)
        self.EditDbBtn.place(x=340, y=110)

        # Gui preparation

    def startApp(self):
        self.mainWindow.mainloop()

    def getItemFromList(self, e):
        selectedItem = self.treeView.focus()
        selectedItem = self.treeView.item(selectedItem, 'values')
        if len(selectedItem) > 1:
            self.basicNameEntry.delete(0, END)
            self.basicNameEntry.insert(0, selectedItem[4])
            self.nameEntry.config(state=NORMAL)
            self.nameEntry.delete(0, END)
            self.nameEntry.insert(0, selectedItem[0])
            self.nameEntry.config(state=DISABLED)
            self.mainWindow.update()

    def saveItemChangeToTable(self):
        selectedItem = self.treeView.focus()
        if selectedItem:
            baseName = self.basicNameEntry.get()
            if baseName not in self.baseNamesList:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    allProdsThread = executor.submit(insertToDB, self.dataBaseCon, baseName,
                                                     'INSERT INTO AllVegNames (Veg_Name)' \
                                                     'VALUES (?);')
                self.baseNamesList.append(baseName)
                self.basicNameComBox['values'] = tuple(self.baseNamesList)
            item = self.treeView.item(selectedItem, 'values')
            item = (item[0], item[1], item[2], item[3], baseName)
            self.treeView.item(selectedItem, values=item)

    def setBasicNameFromComboBox(self, event):
        self.basicNameEntry.delete(0, END)
        self.basicNameEntry.insert(0, self.basicNameComBox.get())

    def saveChangesBtn(self):
        self.hideGuiWidgets()
        data = []
        for child in self.treeView.get_children():
            data.append(tuple(self.treeView.item(child)['values']))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            insertAdminThread = executor.submit(insertAdminData, self.dataBaseCon, data)
            self.loadingAnimation([insertAdminThread])
            self.LastUpdateDateLabel.place(x=270, y=50)
            self.LastUpdateDateLabel['text'] = "Operation COMPLETE last update: " + insertAdminThread.result()
            self.placeGuiWidgets()
            self.mainWindow.update()

    def EditDbBtn(self):
        self.hideGuiWidgets()
        self.treeViewFlag = True
        self.nameEntry.delete(0, END)
        self.basicNameEntry.delete(0, END)
        for i in self.treeView.get_children():
            self.treeView.delete(i)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            allProdsThread = executor.submit(selectFromDB, self.dataBaseCon, 'SELECT * FROM [BraudeProject].[dbo].['
                                                                             'AllProds]')
            workThreads = [allProdsThread]
            self.loadingAnimation(workThreads)
            self.LastUpdateDateLabel.place(x=270, y=50)
            self.placeGuiWidgets()
            for work in workThreads:
                for i, prod in enumerate(work.result()):
                    self.treeView.insert(parent='', index='end', iid=i, values=tuple(prod))
            self.mainWindow.update()

    def updateDataBaseBtn(self):
        self.hideGuiWidgets()
        self.nameEntry.delete(0, END)
        self.basicNameEntry.delete(0, END)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            scrapeThread = executor.submit(importData, self.dataBaseCon, self.baseNamesList)
            self.loadingAnimation([scrapeThread])
            self.LastUpdateDateLabel['text'] = "Operation COMPLETE last update: " + scrapeThread.result()
            self.placeGuiWidgets()
            self.mainWindow.update()

    def placeGuiWidgets(self):
        self.LastUpdateDateLabel.place(x=270, y=50)
        self.UpdateDbBtn.place(x=340, y=78)
        self.EditDbBtn.place(x=340, y=110)
        if self.treeViewFlag:
            self.nameLabel.place(x=560, y=390)
            self.nameEntry.place(x=497, y=420)
            self.baseNameLabel.place(x=400, y=390)
            self.basicNameEntry.place(x=342, y=420)
            self.treeView.place(x=220, y=150)
            self.basicNameComBox.place(x=225, y=420)
            self.comboBoxLabel.place(x=240, y=390)
            self.saveItem.place(x=130, y=418)
            self.saveChangesBtn.place(x=340, y=480)
        self.UpdateDbBtn['state'] = 'active'
        self.EditDbBtn['state'] = 'active'

    def hideGuiWidgets(self):
        self.loadingLabel.place_forget()
        self.treeView.place_forget()
        self.saveChangesBtn.place_forget()
        self.basicNameComBox.place_forget()
        self.saveItem.place_forget()
        self.comboBoxLabel.place_forget()
        self.nameLabel.place_forget()
        self.nameEntry.place_forget()
        self.baseNameLabel.place_forget()
        self.basicNameEntry.place_forget()
        self.LastUpdateDateLabel.grid_forget()
        self.UpdateDbBtn['state'] = 'disable'
        self.EditDbBtn['state'] = 'disable'
        for label in self.LoadingBar:
            label.place_forget()

    def loadingAnimation(self, WorkThreads):
        self.loadingLabel.place(x=375, y=73)
        self.UpdateDbBtn.place(x=340, y=145)
        self.EditDbBtn.place(x=340, y=185)
        for i, label in enumerate(self.LoadingBar):
            label.place(x=(i + 15) * 21, y=100)
        for thread in WorkThreads:
            while thread.running():
                for label in self.LoadingBar:
                    label.config(bg="#FFBD09")
                    time.sleep(0.04)
                    self.mainWindow.update()
                    label.config(bg="#1F2732")
        for label in self.LoadingBar:
            label.place_forget()
