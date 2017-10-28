import tkinter as tk

import chan

class App:

    value_of_combo = 'X'


    def __init__(self, parent):
        self.parent = parent
 
        self.chans = []
        for i in range(4):
            self.chans.append(chan.chan(parent, i))
#        chan2=chan(parent, 1)

 
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()