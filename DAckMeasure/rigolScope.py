import sys
import visa
#import math

class Scope(object):
    """access to the Rigol, and associated tasks"""
    def __init__(self):
        print ("inited")

        #Set up rigel
        self.rm = visa.ResourceManager()
        self.rm.timeout = 200	# Bigger timeout for long mem
        self.rm.chunk_size = 1024000 # Larger chunk of data
        self.connected=False
        self.scope=None
        self.scope=self.connect()
        # Stop the oscilloscope.
        if (self.scope is not None): print("Yes scope")
        else:                        print("Nope scope")
       
    def connect(self):
        if (self.scope is not None):
            return self.scope
        # Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
        instruments = self.rm.list_resources()
        usb = list(filter(lambda x: 'USB' in x, instruments))
        if (len(usb) != 1):
            print ('Bad instrument list', instruments)
            return None

        # Open connection to oscilloscope
        return self.rm.get_instrument(usb[0])

    def measureChan(self, chanNum):
        self.scope.write(":MEAS:SOUR CHAN"+str(chanNum+1))
        return self.scope.query_ascii_values(":MEAS:ITEM? VMAX")[0]
