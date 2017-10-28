import tkinter as tk
from tkinter import ttk

class chan:
    def __init__(self, parent, chan):
        self.startRow=0
        self.startCol=1
        self.parent = parent
        self.combo(chan)

    def combo(self, chan):
        self.box_value = tk.StringVar()
        self.box = ttk.Combobox(self.parent, textvariable=self.box_value)
        self.box['values'] = ('Off', 'Plot 1', 'Plot 2')
        self.box.current(0)
        self.box.grid(column=self.startCol, row=self.startRow+chan)


