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
    
buf = Buffer()
mutex = Semaphore(1)
semProdEven = Semaphore(0)
semProdOdd = Semaphore(0)
semConsEven = Semaphore(0)
semConsOdd = Semaphore(0)

numOfProdEvenWaiting = 0
numOfProdOddWaiting = 0
numOfConsEvenWaiting = 0
numOfConsOddWaiting = 0


def canA1():
    if buf.countAll() < 10:
        return True
    else:
        return False
    
def canA2():
    if buf.countEven()>buf.countOdd():
        return True
    else:
        return False

def canB1():
    if buf.countAll() > 3 and buf.checkLastValue()%2==0:
        return True
    else:
        return False
    
def canB2():
    if buf.countAll() > 7 and buf.checkLastValue()%2==1:
        return True
    else:
        return False

def A1():
    num=0
    global numOfProdEvenWaiting
    global numOfConsEvenWaiting
    global numOfProdOddWaiting
    global numOfConsOddWaiting
    while 1:
        mutex.acquire()
        if not canA1():
            numOfProdEvenWaiting = numOfProdEvenWaiting + 1
            mutex.release()
            semProdEven.acquire()
            numOfProdEvenWaiting = numOfProdEvenWaiting - 1
        print("A1")
        buf.add(num)       
        num=(num+2)%50
        print(buf.printValues())
        print(f"ep: {numOfProdEvenWaiting} op: {numOfProdOddWaiting} ec: {numOfConsEvenWaiting} oc: {numOfConsOddWaiting}")
        if numOfProdOddWaiting>0: # and canA2():
            semProdOdd.release()
        else:
            if numOfConsEvenWaiting>0:# and canB1():
                semConsEven.release()
            else:
                if numOfConsOddWaiting>0:# and canB2():
                    semConsOdd.release()
                else:
                    mutex.release()
        sleep(3)

def A2():
    num=1
    global numOfProdEvenWaiting
    global numOfConsEvenWaiting
    global numOfProdOddWaiting
    global numOfConsOddWaiting
    while 1:
        mutex.acquire()
        if not canA2():
            numOfProdOddWaiting = numOfProdOddWaiting + 1
            mutex.release()
            semProdOdd.acquire()
            numOfProdOddWaiting = numOfProdOddWaiting - 1
        print("A2")
        buf.add(num)       
        num=(num+2)%50
        print(buf.printValues())
        print(f"ep: {numOfProdEvenWaiting} op: {numOfProdOddWaiting} ec: {numOfConsEvenWaiting} oc: {numOfConsOddWaiting}")
        if numOfConsEvenWaiting>0 and canB1():
            semConsEven.release()
        else:
            if numOfConsOddWaiting>0 and canB2():
                semConsOdd.release()
            else:
                if numOfProdEvenWaiting>0 and canA1():
                    semProdEven.release()
                else:
                    mutex.release()
        sleep(3)

def B1():
    global numOfProdEvenWaiting
    global numOfConsEvenWaiting
    global numOfProdOddWaiting
    global numOfConsOddWaiting
    while 1:
        mutex.acquire()
        if not canB1():
            numOfConsEvenWaiting = numOfConsEvenWaiting + 1
            mutex.release()
            semConsEven.acquire()
            numOfConsEvenWaiting = numOfConsEvenWaiting - 1
        print("B1")
        buf.pop()
        print(buf.printValues())
        print(f"ep: {numOfProdEvenWaiting} op: {numOfProdOddWaiting} ec: {numOfConsEvenWaiting} oc: {numOfConsOddWaiting}")
        if numOfConsOddWaiting>0 and canB2():
            semConsOdd.release()
        else:
            if numOfProdEvenWaiting>0 and canA1():
                semProdEven.release()
            else:
                if numOfProdOddWaiting>0 and canA2():
                    semProdOdd.release()
                else:
                    mutex.release()
        sleep(3)

def B2():
    global numOfProdEvenWaiting
    global numOfConsEvenWaiting
    global numOfProdOddWaiting
    global numOfConsOddWaiting
    while 1:
        mutex.acquire()
        if not canB2():
            numOfConsOddWaiting = numOfConsOddWaiting + 1
            mutex.release()
            semConsOdd.acquire()
            numOfConsOddWaiting = numOfConsOddWaiting - 1
        print("B2")
        buf.pop()
        print(buf.printValues())
        print(f"ep: {numOfProdEvenWaiting} op: {numOfProdOddWaiting} ec: {numOfConsEvenWaiting} oc: {numOfConsOddWaiting}")
        if numOfProdEvenWaiting>0 and canA1():
            semProdEven.release()
        else:
            if numOfProdOddWaiting>0 and canA2():
                semProdOdd.release()
            else:
                if numOfConsEvenWaiting>0 and canB1():
                    semConsEven.release()
                else:
                    mutex.release()
        sleep(3)

buf.add(np.random.randint(0, 50))
buf.add(np.random.randint(0, 50))
buf.add(np.random.randint(0, 50))
buf.add(np.random.randint(0, 50))
buf.add(np.random.randint(0, 50))

threadA1 = Thread(target=A1)
threadA2 = Thread(target=A2)
threadB1 = Thread(target=B1)
threadB2 = Thread(target=B2)

# threadA12 = Thread(target=A1)
# threadA22 = Thread(target=A2)
# threadB12 = Thread(target=B1)
# threadB22 = Thread(target=B2)

threadA1.start()
threadA2.start()
threadB1.start()
threadB2.start()

# threadA12.start()
# threadA22.start()
# threadB12.start()
# threadB22.start()

threadA1.join()
threadA2.join()
threadB1.join()
threadB2.join()

# threadA12.join()
# threadA22.join()
# threadB12.join()
# threadB22.join()

