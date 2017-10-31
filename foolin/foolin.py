import sched, time
import random
#class Monitor(object):
#    def __init__(self):
#        self.s = sched.scheduler(time.time, time.sleep)
#        self.lastTime=time.time()
#        self.delay=2
#        self.run=False

#    def do_something(sc): 
#        now=time.time()
#        print("   now= ", now)
#        delt = now-lastTime
#        print("   delta=", delt)
#        lastTime=time.time()
#        if (self.run):
#            self.enter(self.delay, 1, do_something, (sc,))
#        else:
#            self.s.cancel()

#    def start(self):
#        self.s.run()
#        self.run =True
#        self.s.enter(self.delay, 1, self.do_something, (self.s,))
#    def stop(self):
#        self.run =False
import time, os, sys, sched

class Monitor(object):
    def __init__(self):
        self.schedule = sched.scheduler(time.time, time.sleep)
        self.interval = 1
        self._running = False

    #def periodic(self, action, actionargs=()):
    def periodic(self):
        if self._running:
#            self.event = self.schedule.enter(self.interval, 1, self.periodic, (action, actionargs))
            self.event = self.schedule.enter(self.interval, 1, self.periodic, ())
            print("tick")

    def start(self):
        self._running = True
        self.periodic()
        self.schedule.run(False )
        print("start done") 

    def stop(self):
        self._running = False
        if self.schedule and self.event:
            self.schedule.cancel(self.event)
update = Monitor()
update.start()

print("Step 1")
time.sleep(5)
print("Step 2")

for x in range(1,10):
    print(x)
    time.sleep(.5)
print("Step 3")

update.stop()
time.sleep(5)
