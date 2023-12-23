from threading import Thread, Semaphore, Monitor
from time import sleep
import numpy as np

MAXCOUNT = 10

class ConditionVar:
    def __init__(self, value):
        self.variable=value
    
    def wait(self):
        self.variable=self.variable-1

    def signal(self):
        self.variable=self.variable+1

class BufferNode:
    def __init__(self, value):
        self.value=value
        self.next=None

class Buffer:
    def __init__(self):
        self.last=None
    
    def isEmpty(self):
        if(self.last==None):
            return 1
        else:
            return 0
    
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

class MyMonitor(Monitor):
    def __init__(self):
        self.init_lock()

        #deklaracje zmiennych warunkowych:
        self.condProdEven = self.Condition()
        self.condProdOdd = self.Condition()
        self.condConsEven = self.Condition()
        self.condConsOdd = self.Condition()

        #deklaracje zmiennych liczących oczekujące procesy:
        self.numOfProdEvenWaiting=0
        self.numOfProdOddWaiting=0
        self.numOfCondEvenWaiting=0
        self.numOfConsOddWaiting=0
        

myMonitor = MyMonitor()
    
def evenProducer():
    pass

def oddProcuder():
    pass

def evenConsumer():
    pass

def oddConsumer():
    pass


