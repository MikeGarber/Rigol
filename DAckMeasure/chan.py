import tkinter as tk
from tkinter import ttk


class ScopeData(object):
    def __init__(self):
        self.data = []
        self.reset()
        self.plotNum=0
        self.color = 'black'

    def reset(self):
        self.min = self.max = float(0)
        self.samples=0
        del self.data[:]

    def append(self, value):
        if (value < self.min): self.min = value
        if (value > self.max): self.min = value
        self.data.append(value)
        self.samples += 1

class Chan(object):
    def __init__(self, root, scope, chanNum):
        self.startRow=0
        self.startCol=1
        self.chanNum = chanNum  # 0 based
        self.scope = scope
        self.combo(root)
        self.scopeData = ScopeData()
        self.scopeData.color = ['xkcd:yellow', 'xkcd:cyan', 'xkcd:magenta', 'xkcd:blue'][self.chanNum]

    def combo(self, root):
        self.plotSelector = ttk.Combobox(root)
        self.values = ['Off', 'Plot 1', 'Plot 2']
        self.plotSelector['values'] = self.values
        self.plotSelector.current(0)               
        if (self.chanNum==0): self.plotSelector.current(1)      #to ease testing
        if (self.chanNum==2): self.plotSelector.current(2)       #to ease testing
        self.plotSelector.grid(column=self.startCol+1, row=self.startRow+self.chanNum)
        self.timeText = tk.Label(root, text="Chan"+str(self.chanNum+1), justify='left')
        self.timeText.grid(column=self.startCol, row=self.startRow+self.chanNum)

    def reset(self):
        self.scopeData.reset()
        self.plotNum = self.getPlotNum()
        self.scopeData.plotNum = self.plotNum

    def getScopeData(self):
        return self.scopeData

    def setScopeData(self, newFromFileLoad):
        self.scopeData= newFromFileLoad

    def update(self):
#        print("chan", self.chanNum, " self.plotNum", self.plotNum)
        if (self.plotNum==0):
            return
        self.scopeData.append(self.scope.measureChan(self.chanNum))

    def getPlotNum(self):
        if (self.plotSelector.get() == self.values[1]):      return 1
        elif (self.plotSelector.get() == self.values[2]):    return 2
        return 0

