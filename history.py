import threading
import jsonpickle
import datetime
from io import TextIOWrapper,FileIO

class History (object):
    def __init__(self, path : str):
        self.lock = threading.Lock()
        self.path = path
        self.data : dict[str , dict[str , list[str]]] = {}
        self.file : FileIO = FileIO(path, "r+")
        self.load()

    def __del__(self):
        self.file.close()
    
    def load(self):
        # creates or loads the history file
        bytesData = self.file.read()
        strData = bytesData.decode("utf-8")
        print(strData)
        self.data = jsonpickle.decode(strData)

    def save(self):
            jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)
            strData = jsonpickle.encode(self.data, unpicklable=False)
            bytesData = strData.encode("utf-8")
            self.file.seek(0)
            self.file.write(bytesData)

    def AccessUserHistory(self, channelID : int, userID : int)->list[str]:
        channelID = str(channelID)
        userID = str(userID)
        with self.lock:
            if not channelID in self.data:
                self.data[channelID] = {}
            if not userID in self.data[channelID]:
                self.data[channelID][userID] = []
            return self.data[channelID][userID]
        
    def AccessChannelHistory(self, channelID : int)->dict[str , list[str]]:
        channelID = str(channelID)
        with self.lock:
            if not channelID in self.data:
                self.data[channelID] = {}
            return self.data[channelID]
        
    def AddUserHistory(self, channelID : int, userID : int, message : str):
        channelID = str(channelID)
        userID = str(userID)
        with self.lock:
            message = message.strip()
            message = "[" + str(datetime.datetime.now()) + "] " + message
            if not channelID in self.data:
                self.data[channelID] = {}
            if not userID in self.data[channelID]:
                self.data[channelID][userID] = []
            self.data[channelID][userID].append(message)
            self.save()