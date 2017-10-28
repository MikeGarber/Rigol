import tkinter as tk
from tkinter import ttk

class chan:
    def __init__(self, parent, chanNum):
        self.startRow=0
        self.startCol=1
        self.parent = parent
        self.combo(chanNum)

    def combo(self, chanNum):
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value)
        self.box['values'] = ('Off', 'Plot 1', 'Plot 2')
        self.box.current(0)
        self.box.grid(column=self.startCol+1, row=self.startRow+chanNum)
#        timeText = tk.Label(self.parent, text="Chan", justify='left')
        self.timeText = tk.Label(self.parent, text="Chan"+str(chanNum+1), justify='left')
        self.timeText.grid(column=self.startCol, row=self.startRow+chanNum)

