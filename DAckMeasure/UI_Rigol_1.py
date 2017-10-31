import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
import rigolScope, repeatedTimer, chan 
#import numpy 
import matplotlib.pyplot as plt
import datetime, time, matplotlib.dates as mdates
import pickle
import ntpath



class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        container = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.running=False  
        self.elapsed=0
        self.timebase=1      #in Sec !!
        self.setNowTime()
        self.filename=NONE
    
        self.mytimer = repeatedTimer.RepeatedTimer(self.timerUpdateTask)
        scope=rigolScope.Scope()
        self.chans = []
        for i in range(4):
            self.chans.append(chan.Chan(self, scope, i))
 
        vcmd = (self.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.timebaseBox = tk.Entry(self, validate = 'key', validatecommand = vcmd, justify='right')
        self.timebaseBox.insert(0, "1")
        self.timebaseBox.grid(row=4, column=0)
        self.timebaseBox.focus()
        self.startStopButton = tk.Button(self, text="Start", command=self.onstartStopButton)
        self.startStopButton.grid(row=0, column=0)
        self.showDataButton = tk.Button(self, text="Show Data", command=self.onShowDataButton)
        self.showDataButton.grid(row=1, column=0)
        self.timeText = tk.Label(self)      #status??
        self.timeText.grid(row=3, column=0)
        tk.Label(self, text="(Sec)", justify='right').grid(row=4, column=2)
        tk.Label(self, text="Timebase", justify='left').grid(row=4, column=1)
        self.saveFileButton = tk.Button(self, text="SaveFile", command=self.onSaveFileButton)
        self.saveFileButton.grid(row=5, column=0)
        self.loadFileButton = tk.Button(self, text="LoadFile", command=self.onLoadFileButton)
        self.loadFileButton.grid(row=5, column=1)

    def setTime(self, dt):
        self.startDateTime = dt
        self.startDateTimeStr = self.startDateTime.strftime("%m_%d_%Y__%H_%M_%S")
########### def roundTimeNow(): ############
        roundTo=1        #roundTo : Closest number of seconds to round to.
        dt = datetime.datetime.now()
        seconds = (dt - dt.min).seconds
        # // is a floor division, not a comment on following line:
        rounding = (seconds + roundTo / 2) // roundTo * roundTo
        self.startTimeRounded  = dt + datetime.timedelta(0,rounding - seconds,-dt.microsecond)
########################################
    def setNowTime(self):
        self.setTime(datetime.datetime.now())

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if(action=='1'):
            if text in '0123456789.':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError: return False
            else: return False
        else: return True
    
    def onstartStopButton(self):
        if (not self.running):      #if Starting Now !!!!!
            try:        #validate the value before s
                self.timebase=float(self.timebaseBox.get()) #in Sec
            except ValueError: return False
            self.elapsed=0
            
            for i in range(4):
                self.chans[i].reset()

            self.setNowTime( )
            self.mytimer.start(self.timebase)
            self.filename=NONE
        else:
            self.mytimer.stop()
        self.startStopButton.config(text=("Stop", "Start")[self.running])
        self.running= not self.running
            
    def onSaveFileButton(self):
        name = asksaveasfilename(initialdir=".", filetypes =(("Rigol Data", "*.rigol"),("All Files","*.*")), initialfile=str(self.startDateTimeStr+".rigol"))
        if (name):
            try:
                with open(name, 'wb') as f:  
                    pickle.dump(self.timebase, f)
                    pickle.dump(self.startDateTime, f)
                    for i in range(4):
                        sd = self.chans[i].getScopeData()
                        pickle.dump(sd, f)
            except IOError as e:
               print( "I/O error({0}): {1}".format(e.errno, e.strerror))
            except: #handle other exceptions such as attribute errors
               print( "Unexpected error:", sys.exc_info()[0])
            f.close()

    def onLoadFileButton(self):
        name = askopenfilename(initialdir=".", filetypes =(("Rigol Data", "*.rigol"),("All Files","*.*")) ) 
        if (name):
            try:
                with open(name, 'rb') as f:  
                    self.timebase = pickle.load(f)      
                    sv=StringVar()
                    sv.set(str(self.timebase))
                    self.timebaseBox.config(text=sv)
                    x=pickle.load(f)
                    self.setTime(x)
                    for i in range(4):
                        self.chans[i].setScopeData(pickle.load(f))
                    head, tail = ntpath.split(name)
                    self.filename=tail or ntpath.basename(head)
            except IOError as e:
               print( "I/O error({0}): {1}".format(e.errno, e.strerror))
            except: #handle other exceptions such as attribute errors
               print( "Unexpected error:", sys.exc_info()[0])

    def onShowDataButton(self):
        scopeDatas = []      #array of scopeData
        sampSize=0
        for i in range(4):
            sd = self.chans[i].getScopeData()
            scopeDatas.append(sd)
            if (sd.samples):
                sampSize = sd.samples
        time = [self.startTimeRounded + (datetime.timedelta(seconds=i)*self.timebase) for i in range(sampSize)]
        
        vals = [0,0,0]      ## 1 plot or 2???
        for i in range(4):
            vals[scopeDatas[i].plotNum] +=1
        numplots=0
        if (vals[0]==4):            return
        elif (vals[2] & vals[1]):   numplots = 2
        else:                       numplots = 1
        fig, (plots) = plt.subplots(1,numplots)

        for plot in range(1,3): # 1 & 2;  plots might not be an array
            if (numplots==1):       subplot = plots
            else:                   subplot=plots[plot-1]
            for i in range(4):
                sd = scopeDatas[i]
                if(sd.plotNum==plot):
                    print("sd data - ", sd.data)
                    subplot.plot(time, sd.data, sd.color)  
            subplot.xaxis.set_major_formatter( mdates.DateFormatter('%H:%M:%S'))
        fig.autofmt_xdate(rotation=90, ha='center')
        secondline= "\n"+self.filename if (self.filename) else ""
        plt.suptitle(str(self.startTimeRounded)+secondline)
        plt.show()
        plt.close()

    def timerUpdateTask(self):
        self.elapsed += self.timebase
        self.timeText.config(text=self.elapsed)
        for i in range(4):
            self.chans[i].update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rigol Data Acquisition Tool Ver 1.0")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
