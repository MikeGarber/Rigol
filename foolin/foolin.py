import tkinter as tk
import os
import importedChan

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        container = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        tk.Button(self, text="main app").grid(row=0, column=0)
        self.chanFunction()       #col=1, works fine, without the class included
        sameModuleChan(self)      #col=2        
        importedChan.importedChan(self)     #col=3 including this is ??

    def chanFunction(root):
        tk.Button(root, text="chanFunction").grid(row=0, column=1)


class sameModuleChan():
    def __init__(self, parent):
        tk.Button(parent, text="sameModuleChan").grid(row=0, column=2)

if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()