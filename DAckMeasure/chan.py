import tkinter as tk
from tkinter import ttk

class chan(object):
    def __init__(self, root, chanNum):
        self.startRow=0
        self.startCol=1
        self.chanNum = chanNum
        self.combo(root)
        self.scopeData = []

    def combo(self, root):
        self.box = ttk.Combobox(root)
        self.values = ['Off', 'Plot 1', 'Plot 2']
        self.box['values'] = self.values#('Off', 'Plot 1', 'Plot 2')
        self.box.current(0)
        self.box.grid(column=self.startCol+1, row=self.startRow+self.chanNum)
        self.timeText = tk.Label(root, text="Chan"+str(self.chanNum+1), justify='left')
        self.timeText.grid(column=self.startCol, row=self.startRow+self.chanNum)

    def reset(self):
        del self.scopeData[:]
        self.tstCounter=0
        print("**** reset")
        self.boxText = self.getSetting()

    def getSetting(self):
        return self.box.get()

    def getData(self):
        return self.scopeData

    def update(self):
        if (self.boxText == self.values[0]):
            return
        self.scopeData.append(self.chanNum*self.tstCounter)
        self.tstCounter += 1
        if (self.boxText == self.values[1]):
            print("Plot 1 update chan "+ str(self.chanNum+1))
        elif (self.boxText == self.values[2]):
            print("Plot 2 update chan "+ str(self.chanNum+1))
