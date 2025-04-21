import collections

class Logger(object):
  
    def __init__(self):
        self.Verbosity = 1


    @staticmethod
    def Log(msg):
        print(msg)