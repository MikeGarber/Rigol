
import datetime

def roundTimeNow():
   roundTo=1        #roundTo : Closest number of seconds to round to.
   dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   # // is a floor division, not a comment on following line:
   rounding = (seconds + roundTo / 2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding - seconds,-dt.microsecond)

