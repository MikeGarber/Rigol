
#from tkinter import *
import tkinter as tk
import os
import DAckMeasure

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        container = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.running=False  ##should be from the non gui??
        self.elapsed=0
        self.timebase=1000

        scope=DAckMeasure.DAckMeasure()
        self.chans = []
        for i in range(4):
            self.chans.append(tk.IntVar())
        self.startButton = tk.Button(self, text="Start/Restart", command=self.onStartButton)
        self.startButton.grid(row=0, column=0)
        self.pauseResumeButton = tk.Button(self, text="Pause", state=tk.DISABLED, command=self.onPauseResumeButton)
        self.pauseResumeButton.grid(row=1, column=0)
        self.showDataButton = tk.Button(self, text="Show Data", command=self.onShowDataButton)
        self.showDataButton.grid(row=2, column=0)
        self.Chan1Button = tk.Checkbutton(self, text="Chan 1", variable=self.chans[0])
        self.Chan1Button.grid(row=0, column=1)
        self.Chan2Button = tk.Checkbutton(self, text="Chan 2", variable=self.chans[1])
        self.Chan2Button.grid(row=1, column=1)
        self.Chan3Button = tk.Checkbutton(self, text="Chan 3", variable=self.chans[2])
        self.Chan3Button.grid(row=2, column=1)
        self.Chan4Button = tk.Checkbutton(self, text="Chan 4", variable=self.chans[3])
        self.Chan4Button.grid(row=3, column=1)
        self.timeText = tk.Label(self)
        self.timeText.grid(row=3, column=0)

        vcmd = (self.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.timebaseBox = tk.Entry(self, validate = 'key', validatecommand = vcmd, justify='right', text="0")
        self.timebaseBox.grid(row=4, column=0)
        self.timebaseBox.focus()
        self.timeText = tk.Label(self, text="Sec", justify='left')
        self.timeText.grid(row=4, column=1)

        self.onTimeUpdate()

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text in '0123456789':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
    
    def onStartButton(self):
        self.running=True
        self.elapsed=0
        self.startButton.config(state=tk.DISABLED)
        self.pauseResumeButton.config(state=tk.NORMAL, text="Pause")
        self.timebase=int(self.timebaseBox.get())*1000

    def onPauseResumeButton(self):
        PauseButTxt="Pause"
        runningState=True
        startButEnab=tk.DISABLED
        if (self.running):
            PauseButTxt="Resume"
            runningState=False
            startButEnab=tk.NORMAL
        self.pauseResumeButton.config(text=PauseButTxt)
        self.startButton.config(state=startButEnab)
        self.running=runningState

    def onShowDataButton(self):
        pass

    def onTimeUpdate(self):
        if (self.running):
            self.elapsed += self.timebase
            self.timeText.config(text=self.elapsed)
        self.after(self.timebase, self.onTimeUpdate)

#########################################
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rigol Data Acquisition Tool Ver 0.0")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    


