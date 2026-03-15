
import collections
import json
from ..tracer import Logger

class Parser(object):
  
    def __init__(self, path: str):
        self.Path = path

    def deserializeProject(self):
        Logger.Log("Deserialize: " + str(self.Path))
