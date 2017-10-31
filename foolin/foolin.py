class scopeData(object):
    def __init__(self, data):
        self.data = data

    def reset():
        del self.data[:]

class chan(object):
    def __init__(self, data):
        self.scopeData = scopeData(data)


    def getScopeData(self):
        return self.scopeData

    def setScopeData(self, newFromFileLoad):
#        del self.scopeData
        self.scopeData= newFromFileLoad



chans = []
for i in range(4):
    chans.append(chan([1,2,3,4]))

print(type(chans))
print(type(chans[0]))
sdNew = scopeData([5,6,7])
chans[0].setScopeData(sdNew)
sdCheck = chans[0].getScopeData()

print(type(chans[1]))
sd2 = chans[1].getScopeData()
chans[1].setScopeData(sd2)
