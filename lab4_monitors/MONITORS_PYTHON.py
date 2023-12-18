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


class Monitor:
    def __init__(self):
        self.x = ConditionVar(1)
        self.y = ConditionVar(1)
        self.count = 0
        self.buffer = Buffer()

    def enter(self, item):
        if self.count == MAXCOUNT:
            self.x.wait()
        self.buffer.add(item)
        self.count = self.count + 1
        if self.count == 1:
            self.y.signal()

    def remove(self):
        if self.count == 0:
            self.y.wait()
        self.buffer.pop()
        self.count = self.count - 1
        if self.count == MAXCOUNT - 1:
            self.x.signal()
        
    

monitorBuffer = Monitor()

