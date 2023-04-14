class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next



class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, data):
        if self.head is None:
            self.head = Node(data)
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = Node(data)

    def remove(self, data):
        current = self.head
        if current.data == data:
            self.head = current.next
            return
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def printList(self):
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next

    def delete(self, data):
        current = self.head
        if current.data == data:
            self.head = current.next
            return
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next
    
    def search(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def getSize(self):
        return self.size
    
    def isEmpty(self):
        return self.head is None
    
    def clear(self):
        self.head = None

    def push(self, data):
        self.insert(data)
    
    def pop(self, data):
        self.remove(data)


class sortedLinkedList:
    def __init__(self):
        self.head = None
    
    def add_data(self, data):
        if self.head is None:
            self.head = Node(data)
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = Node(data)