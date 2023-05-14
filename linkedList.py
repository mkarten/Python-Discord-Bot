class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self,head=None,current=None,last_element=None):
        self.head = head
        self.current = current
        self.last_element = last_element

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.current = new_node
        else:
            new_node.prev = self.current
            self.current.next = new_node
            self.current = new_node
        self.last_element = new_node

    def move_forward(self):
        if self.current.next is not None:
            self.current = self.current.next

    def move_backward(self):
        if self.current.prev is not None:
            self.current = self.current.prev

    def convert_to_list(self):
        node = self.head
        list = []
        while node:
            list.append(node.data)
            node = node.next
        return list

    def convert_from_list(self, list):
        for i in list:
            self.add_node(i)
    
    def clear(self):
        self.head = None
        self.current = None
        self.last_element = None

    def __iter__(self):
        node = self.head
        if node is None:
            print("No history")
            yield []
            return
        while node:
            yield node.data
            node = node.next

    def __getstate__(self):
        if self.head is None:
            return ["N33d2C0nvert"]
        return self.convert_to_list()
