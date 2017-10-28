

#!/usr/bin/python
"""
Download data from Rigol MSO1104 and graph with matplot lib.
This one uses the raw data from the internal memory.
Python35 & PyVISA 1.8 used.
Written by Stevanx

Based on http://righto.com/rigol  
By Ken Shirriff
Which is based on http://www.cibomahto.com/2010/04/controlling-a-rigol-oscilloscope-using-linux-and-python/
by Cibo Mahto.
"""

import numpy
import matplotlib.pyplot as plot
import sys
import visa
import math

rm = visa.ResourceManager()
rm.timeout = 20000	# Bigger timeout for long mem
rm.chunk_size = 1024000 # Larger chunk of data

# Get the USB device, e.g. 'USB0::0x1AB1::0x0588::DS1ED141904883'
instruments = rm.list_resources()
usb = list(filter(lambda x: 'USB' in x, instruments))
if (len(usb) != 1):
    print ('Bad instrument list', instruments)
    sys.exit(-1)

# Open connection to oscilloscole
scope = rm.get_instrument(usb[0])
# Stop the oscilloscope.
scope.write(":STOP")

#### This is the part that extracts the waveform from the scope.
# Query the sample rate
sample_rate = scope.query_ascii_values(':ACQ:SRAT?')[0]
# Select CH1
scope.write(":WAV:SOUR CHAN1")

# Y origin for wav data
YORigin = scope.query_ascii_values(":WAV:YOR?")[0]
# Y REF for wav data
YREFerence = scope.query_ascii_values(":WAV:YREF?")[0]
# Y INC for wav data
YINCrement = scope.query_ascii_values(":WAV:YINC?")[0]

# X origin for wav data
XORigin = scope.query_ascii_values(":WAV:XOR?")[0]
# X REF for wav data
XREFerence = scope.query_ascii_values(":WAV:XREF?")[0]
# X INC for wav data
XINCrement = scope.query_ascii_values(":WAV:XINC?")[0]

# Get time base to calculate memory depth.
time_base = scope.query_ascii_values(":TIM:SCAL?")[0]
# Calculate memory depth for later use.
memory_depth = (time_base*12) * sample_rate 
memory_depth /= 10#speed things up here!!
print ('Plotting1')
print ('WEVE HACKED THE MEMORY DEPTH BY A FACTOR OF 10 to speed things up')

# Set the waveform reading mode to RAW.
scope.write(":WAV:MODE RAW")
# Set return format to Byte.
scope.write(":WAV:FORM BYTE")

# Set waveform read start to 0.
scope.write(":WAV:STAR 1")
# Set waveform read stop to 250000.
scope.write(":WAV:STOP 250000")

# Read data from the scope, excluding the first 9 bytes (TMC header).
rawdata = scope.query_binary_values(":WAV:DATA?", datatype='B')

# Check if memory depth is bigger than the first data extraction.
if (memory_depth > 250000):
	loopcount = 1
	# Find the maximum number of loops required to loop through all memory.
	loopmax = math.ceil(memory_depth/250000)
	while (loopcount < loopmax):
		# Calculate the next start of the waveform in the internal memory.
		start = (loopcount*250000)+1
		scope.write(":WAV:STAR {0}".format(start))
		# Calculate the next stop of the waveform in the internal memory
		stop = (loopcount+1)*250000
		print(stop)
		scope.write(":WAV:STOP {0}".format(stop))
		# Extent the rawdata variables with the new values.
		rawdata.extend(scope.query_binary_values(":WAV:DATA?", datatype='B'))
		loopcount = loopcount+1

		
#### This is the part that extracts the measurements from the scope.
# Measure on channel 1.
scope.write(":MEAS:SOUR CHAN1")
# Grab VMAX
v_max = scope.query_ascii_values(":MEAS:ITEM? VMAX")
v_min = scope.query_ascii_values(":MEAS:ITEM? VMIN")
v_pp = scope.query_ascii_values(":MEAS:ITEM? VPP")
v_rms = scope.query_ascii_values(":MEAS:ITEM? VRMS")
v_avg = scope.query_ascii_values(":MEAS:ITEM? VAVG")
freq = scope.query_ascii_values(":MEAS:ITEM? FREQ")

#print ('Vmax: {0}\nVmin: {1}\nVpp: {2}\nVrms: {3}\nVavg: {4}\nFreq: {5}'.format(v_max[0],v_min[0],v_pp[0],v_rms[0],v_avg[0],freq[0]))

#### This is the part that handles all the data and presents it nicely.
# Close connection to scope.
scope.close()

# Convert byte to actual voltage using Rigol data
data = (numpy.asarray(rawdata) - YORigin - YREFerence) * YINCrement
# Calcualte data size for generating time axis
data_size = len(data)
# Create time axis
time = numpy.linspace(XREFerence, XINCrement*data_size, data_size)

# Inform about the data size, sample rate and scope setings. Mostly used for debugging.
print ('time_base=', time_base, 'Data size:', data_size, "Sample rate:", sample_rate)
print ('YORigin:', YORigin, 'YREFerence:', YREFerence, 'YINCrement:', YINCrement)
print ('XORigin:', XORigin, 'XREFerence:', XREFerence, 'XINCrement:', XINCrement)

# See if we should use a different time axis
baseindex=0 #was -1
if (time[baseindex] < 1e-3):
    time = time * 1e6
    tUnit = "uS"
elif (time[baseindex] < 1):
    time = time * 1e3
    tUnit = "mS"
else:
	tUnit = "S"

# Inform about the data size, sample rate and scope setings. Mostly used for debugging.
print ('Data size:', data_size, "Sample rate:", sample_rate)
print ('YORigin:', YORigin, 'YREFerence:', YREFerence, 'YINCrement:', YINCrement)
print ('XORigin:', XORigin, 'XREFerence:', XREFerence, 'XINCrement:', XINCrement)

# Graph data with pyplot.
plot.plot(time, data)
#plot.title("Oscilloscope Channel 1")
plot.ylabel("Voltage (V)")
plot.xlabel("Time (" + tUnit + ")")
##plot.xlim(time[baseindex+1], time[baseindex])
plot.subplots_adjust(left=0.1,top=0.98,bottom=0.1,right=0.8)
plot.text(0.81, 0.5, 'Vmax: {0}V\nVmin: {1}V\nVpp: {2}V\nVrms: {3}V\nVavg: {4}V\nFreq: {5}Hz'.format(v_max[0],v_min[0],v_pp[0],v_rms[0],v_avg[0],freq[0]), style='italic', bbox={'facecolor':'white', 'alpha':0.1, 'pad':0},transform=plot.gcf().transFigure)
plot.show()
