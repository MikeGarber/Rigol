import pickle


class Ex(object):
    def __init__(self, o1, o2):
        self.o1=o1
        self.o2=o2
class Wy(object):
    def __init__(self, o1, o2):
        self.y1=o1
        self.y2=o2

X=Ex("Hi Mom", (2,4,6,8))
Y=Wy((1,3,5,7,9), "Hello World")

with open('entry.pickle', 'wb') as f:  
    pickle.dump(X, f)              
    pickle.dump(Y, f)              
    f.close()


with open('entry.pickle', 'rb') as g:  
    X1 = pickle.load(g) 
    Y1 = pickle.load(g) 

print(X1)
print(X1.o1, X1.o2)
print(Y1.y1, Y1.y2)