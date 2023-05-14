import jsonpickle
from HistoryLock import HistoryLock
from linkedList import LinkedList
from HashTable import HashTable
import datetime
from io import FileIO

class History (object):
    def __init__(self, path : str):
        self.lock = HistoryLock()
        self.path = path
        self.data = HashTable()
        try:
            self.file : FileIO = FileIO(path, "r+")
        except FileNotFoundError:
            f = open(path, "w+")
            f.write("{\n}")
            f.close()
            self.file : FileIO = FileIO(path, "r+")
        
        self.load()

    def __del__(self):
        self.file.close()
    
    def load(self):
        # creates or loads the history file
        bytesData = self.file.read()
        strData = bytesData.decode("utf-8")
        tempData = jsonpickle.decode(strData)
        for key in tempData:
            tempLinkedList = LinkedList()
            tempLinkedList.convert_from_list(tempData[key])
            self.data[key] = tempLinkedList

    def save(self):
            jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
            strData = jsonpickle.encode(self.data, unpicklable=False)
            strData = strData.replace("\"N33d2C0nvert\"", "")
            bytesData = strData.encode("utf-8")
            self.file.seek(0)
            self.file.truncate()
            self.file.write(bytesData)

    def AccessUserHistory(self, userID : int)->list[str]:
        userID = str(userID)
        with self.lock:
            if not userID in self.data:
                self.data[userID] = LinkedList()
            if self.data[userID].head is None:
                return []
            return self.data[userID]
        
        
    def AddUserHistory(self, userID : int, message : str):
        userID = str(userID)
        with self.lock:
            message = message.strip()
            message = "[" + str(datetime.datetime.now()) + "] " + message
            if not userID in self.data:
                self.data[userID] = LinkedList()
            self.data[userID].add_node(message)
            self.save()

    def GetLastCommand(self, userID : int)->str:
        userID = str(userID)
        with self.lock:
            if not userID in self.data:
                self.data[userID] = LinkedList()
                return "You have no history"
            data = self.data[userID].last_element
            if data is None:
                return "You have no history"
            return data.data
            
    def GetCurrentCommand(self, userID : int)->str:
        userID = str(userID)
        with self.lock:
            if not userID in self.data:
                self.data[userID] = LinkedList()
                return "You have no history"
            data = self.data[userID].current
            if data is None:
                return "You have no history"
            return data.data
        
    def GoBackward(self, userID : int):
        userID = str(userID)
        with self.lock:
            if not userID in self.data:
                self.data[userID] = LinkedList()
            self.data[userID].move_backward()
    
    def GoForward(self, userID : int):
        userID = str(userID)
        with self.lock:
            if not userID in self.data:
                self.data[userID] = LinkedList()
            self.data[userID].move_forward()

    def Clear(self, userID : int):
        userID = str(userID)
        with self.lock:
            if not userID in self.data:
                self.data[userID] = LinkedList()
            self.data[userID].clear()
            self.save()