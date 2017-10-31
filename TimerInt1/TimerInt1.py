from threading import Timer
import time

class RepeatedTimer(object):
    def __init__(self, function, *args, **kwargs):
        self._timer     = None
        self.interval   = 0
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.lastTime=time.time()
        self.is_running = False
#        self.start()

    def _execute(self):
        if not self.is_running:
            self.stop()
        else:
            now=time.time()
#            print("   now= ", now)
            delt = self.lastTime - now +2*self.interval
            print("   delta=", delt)
            if (delt<0): print("OVERRUN!!!")
            self.lastTime=now

            self._start(delt)   #do it again, Tony
            print("task")
            self.function(*self.args, **self.kwargs)

    def _start(self, interval):
        self._timer = Timer(interval, self._execute)
        self._timer.start()
        self.is_running = True

    def start(self, interval):
        self.interval   = interval
        self._start(self.interval)

    def stop(self):
        self._timer.cancel()
        self.is_running = False

from time import sleep

def hi():
    print("hi")

print( "starting...")
rt = RepeatedTimer(hi) 
rt.start(1)
try:
    sleep(5) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!