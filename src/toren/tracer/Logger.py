import collections
import uuid

class Logger(object):
  
    def __init__(self):
        self.Verbosity = 1
        self.ID = str(uuid.uuid4())


    @staticmethod
    def Log(msg):
        print(msg)