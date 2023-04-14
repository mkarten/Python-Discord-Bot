from node import node

class fifo:
    def __init__(self, data):
        self.head = node(data)
        self.tail = self.head
        self.size = 1
    
    def __str__(self):
        return str(self.head)
    
    def push(self, data):
        self.tail.next = node(data)
        self.tail = self.tail.next
        self.size += 1
    
    def pop(self):
        if self.head == None:
            return None
        else:
            value = self.head.value
            self.head = self.head.next
            self.size -= 1
            return value
    
    def peek(self):
        if self.head == None:
            return None
        else:
            return self.head.value
     
    def __sizeof__(self) -> int:
        return self.size

    def size(self):
        return self.size


