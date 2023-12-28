from threading import Thread, Semaphore
from time import sleep
import numpy as np


class BufferNode:
    def __init__(self, value):
        self.value=value
        self.next=None

class Buffer:
    def __init__(self):
        self.last=None
    
    def isEmpty(self):
        if(self.last==None):
            return True
        else:
            return False
    
    def add(self, value):
        node = BufferNode(value)
        if(self.isEmpty()):
            self.last=node
        else:
            temp=self.last
            while temp.next!=None:
                temp=temp.next
            temp.next=node
    
    def pop(self):
        if(self.isEmpty()):
            print("Buffer is empty, you cannot pop an item")
            return -1
        else:
            itemToPop=self.last.value
            self.last=self.last.next
            return itemToPop
        
    def checkLastValue(self):
        if(self.isEmpty()):
            print("Buffer is empty")
            return None
        return self.last.value
    
    def countAll(self):
        temp = self.last
        count = 0
        while temp!=None:
            count=count+1
            temp = temp.next
        return count
    
    def countEven(self):
        temp = self.last
        count = 0
        while temp!=None:
            if(temp.value%2==0):
                count=count+1
            temp = temp.next
        return count

    def countOdd(self):
        temp = self.last
        count = 0
        while temp!=None:
            if(temp.value%2==1):
                count=count+1
            temp = temp.next
        return count
    
    def printValues(self):
        temp=self.last
        values=[]
        while temp!=None:
            values.append(temp.value)
            temp=temp.next
        return values

class Condition:
    def __init__(self, value):
        self.waitingCount=0
        self.var=Semaphore(value)

    def wait(self):
        self.var.acquire()

    def signal(self):
        if self.waitingCount>0:
            self.waitingCount=self.waitingCount-1
            self.var.release()
            return True
        else:
            return False
        

class MyMonitor:
    def __init__(self):
        #deklaracje zmiennych warunkowych:
        self.condProdEven = Condition(0)
        self.condProdOdd = Condition(0)
        self.condConsEven = Condition(0)
        self.condConsOdd = Condition(0)

        self.buffer=Buffer()
        self.s=Semaphore(1)

    def enter(self):
        self.s.acquire()

    def leave(self):
        self.s.release()

    def wait(self, cond):
        cond.waitingCount=cond.waitingCount+1
        self.leave()
        cond.wait()
    
    def signal(self, cond):
        if cond.signal():
            self.enter()

    def putEven(self, item):
        self.enter()
        print(f"EP: {self.buffer.printValues()}")
        if (not self.buffer.countAll()<10):
            self.wait(self.condProdEven)
        self.buffer.add(item)
        if (self.condConsEven.waitingCount>0 and self.buffer.countAll() > 3 and self.buffer.checkLastValue()%2==0):
            self.signal(self.condConsEven)
        elif(self.condProdOdd.waitingCount>0 and self.buffer.countEven()>self.buffer.countOdd()):
            self.signal(self.condProdOdd)
        elif(self.condConsOdd.waitingCount>0 and self.buffer.countAll() > 7 and self.buffer.checkLastValue()%2==1):
            self.signal(self.condConsOdd)
        self.leave()

    def putOdd(self, item):
        self.enter()
        print(f"OP: {self.buffer.printValues()}")
        if (not self.buffer.countEven()>self.buffer.countOdd()):
            self.wait(self.condProdOdd)
        self.buffer.add(item)
        if (self.condConsOdd.waitingCount>0 and self.buffer.countAll() > 7 and self.buffer.checkLastValue()%2==1):
            self.signal(self.condConsOdd)
        elif(self.condConsEven.waitingCount>0 and self.buffer.countAll() > 3 and self.buffer.checkLastValue()%2==0):
            self.signal(self.condConsEven)
        elif (self.condProdEven.waitingCount>0 and self.buffer.countAll()<10):
            self.signal(self.condProdEven)
        self.leave()

    def getEven(self):
        self.enter()
        print(f"EC: {self.buffer.printValues()}")
        if not (self.buffer.countAll() > 3 and self.buffer.checkLastValue()%2==0):
            self.wait(self.condConsEven)
        self.buffer.pop()
        if (self.condProdEven.waitingCount>0 and self.buffer.countAll()<10):
            self.signal(self.condProdEven)
        elif(self.condConsOdd.waitingCount>0 and self.buffer.countAll() > 7 and self.buffer.checkLastValue()%2==1):
            self.signal(self.condConsOdd)
        elif (self.condProdOdd.waitingCount>0 and self.buffer.countEven()>self.buffer.countOdd()):
            self.signal(self.condProdOdd)
        self.leave()

    def getOdd(self):
        self.enter()
        print(f"OC: {self.buffer.printValues()}")
        if not (self.buffer.countAll() > 7 and self.buffer.checkLastValue()%2==1):
            self.wait(self.condConsOdd)
        self.buffer.pop()
        if(self.condProdOdd.waitingCount>0 and self.buffer.countEven()>self.buffer.countOdd()):
            self.signal(self.condProdOdd)
        elif (self.condProdEven.waitingCount>0 and self.buffer.countAll()<10):
            self.signal(self.condProdEven)
        elif(self.condConsEven.waitingCount>0 and self.buffer.countAll() > 3 and self.buffer.checkLastValue()%2==0):
            self.signal(self.condConsEven)
        self.leave()


myMonitor = MyMonitor()

myMonitor.buffer.add(np.random.randint(0,50))
myMonitor.buffer.add(np.random.randint(0,50))
myMonitor.buffer.add(np.random.randint(0,50))
myMonitor.buffer.add(np.random.randint(0,50))
myMonitor.buffer.add(np.random.randint(0,50))
    
def evenProducer():
    num=0
    while True:
        myMonitor.putEven(num)
        sleep(1)
        num=(num+2)%50

def oddProcuder():
    num=1
    while True:
        myMonitor.putOdd(num)
        sleep(1)
        num=(num+2)%50

def evenConsumer():
    while True:
        myMonitor.getEven()
        sleep(1)

def oddConsumer():
    while True:
        myMonitor.getOdd()
        sleep(1)




thread_EP=Thread(target=evenProducer)
thread_OP=Thread(target=oddProcuder)
thread_EC=Thread(target=evenConsumer)
thread_OC=Thread(target=oddConsumer)

# thread_EP2=Thread(target=evenProducer)
# thread_OP2=Thread(target=oddProcuder)
# thread_EC2=Thread(target=evenConsumer)
# thread_OC2=Thread(target=oddConsumer)

thread_EP.start()
thread_OP.start()
thread_EC.start()
thread_OC.start()

# thread_EP2.start()
# thread_OP2.start()
# thread_EC2.start()
# thread_OC2.start()

thread_EP.join()
thread_OP.join()
thread_EC.join()
thread_OC.join()

# thread_EP2.join()
# thread_OP2.join()
# thread_EC2.join()
# thread_OC2.join()