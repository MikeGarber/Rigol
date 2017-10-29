import tkinter as tk
from tkinter import ttk

class chan(object):
    def __init__(self, root, scope, chanNum):
        self.startRow=0
        self.startCol=1
        self.chanNum = chanNum
        self.scope = scope
        self.combo(root)
        self.scopeData = scopeData()

    def combo(self, root):
        self.plotSelector = ttk.Combobox(root)
        self.values = ['Off', 'Plot 1', 'Plot 2']
        self.plotSelector['values'] = self.values#('Off', 'Plot 1', 'Plot 2')
        self.plotSelector.current(0)
        self.plotSelector.grid(column=self.startCol+1, row=self.startRow+self.chanNum)
        self.timeText = tk.Label(root, text="Chan"+str(self.chanNum+1), justify='left')
        self.timeText.grid(column=self.startCol, row=self.startRow+self.chanNum)

    def reset(self):
        self.scopeData.reset()
        self.tstCounter=0
        self.plotNum = self.getPlotNum()
        self.scopeData.plotNum = self.plotNum

    def getScopeData(self):
        return self.scopeData

    def update(self):
        if (self.plotNum==0):
            return
        self.scopeData.append(self.scope.measureChan(self.chanNum))

    def getPlotNum(self):
        if (self.plotSelector.get() == self.values[1]):
            return 1
        elif (self.plotSelector.get() == self.values[2]):
            return 2
        return 0

class scopeData(object):
    def __init__(self):
        self.data = []
        self.reset()
        self.plotNum=0

    def reset(self):
        self.min = self.max = 0
        del self.data[:]

    def append(self, value):
        self.data.append(value)

