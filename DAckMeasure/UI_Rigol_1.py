import tkinter as tk
import os
import DAckMeasure
import chan
#import date
import datetime

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        container = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.running=False  ##should be from the non gui??
        self.elapsed=0
        self.timebase=1000

        scope=DAckMeasure.DAckMeasure()
        self.StartStopButton = tk.Button(self, text="Start", command=self.onStartStopButton)
        self.StartStopButton.grid(row=0, column=0)
        self.showDataButton = tk.Button(self, text="Show Data", command=self.onShowDataButton)
        self.showDataButton.grid(row=1, column=0)
 
        self.chans = []
        for i in range(4):
            self.chans.append(chan.chan(self, i))
 
        self.timeText = tk.Label(self)      #status??
        self.timeText.grid(row=3, column=0)

        vcmd = (self.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.timebaseBox = tk.Entry(self, validate = 'key', validatecommand = vcmd, justify='right')
        self.timebaseBox.insert(0, "1")
#        self.timebaseBox.config(text="1")
        self.timebaseBox.grid(row=4, column=0)
        self.timebaseBox.focus()

        tk.Label(self, text="(Sec)", justify='right').grid(row=4, column=2)
        tk.Label(self, text="Timebase", justify='left').grid(row=4, column=1)

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            if text in '0123456789.':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
    
    def onStartStopButton(self):
        self.StartStopButton.config(text=("Stop", "Start")[self.running])
        self.running= not self.running
        if (self.running):      #if Starting Now !!!!!
            self.timebase=int(float(self.timebaseBox.get())*1000)
            print("starting.....")
            for i in range(4):
                self.chans[i].reset()

            self.onTimeUpdate()     #1st update; will perpetuatethe rest

            self.startDateTime = datetime.datetime.now()
            print(self.startDateTime)
            
    def onShowDataButton(self):
           for i in range(4):
                data = self.chans[i].getData()
                print(data)

    def onTimeUpdate(self):
        if (self.running):      
            self.elapsed += self.timebase/1000
            self.timeText.config(text=self.elapsed)
            for i in range(4):
                self.chans[i].update()
            self.after(self.timebase, self.onTimeUpdate)

#########################################
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rigol Data Acquisition Tool Ver 0.0")
    MainApplication(root).pack(side="top", fill="both", expand=True)
#    MainApplication(root)
    root.mainloop()
    


