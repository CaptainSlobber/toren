from .Module import Module

import collections
import json
from typing import List


class ModuleCollection():

    def getType(self):
        return "toren.ModuleCollection"
    
    def __init__(self):
        self.Data = collections.OrderedDict()
    
    def initialize(self, modulelist: List[Module] = [], parentproject = None):
        self.from_list(modulelist, parentproject)
        return self

    def removeModule(self, key):
        if key in self.Data:
            del self.Data[key]


    def getItem(self, id):
        if id in self.Data:
            return self.Data[id]
        return None
    
    def addModule(self, module, parentproject):
        if isinstance(module, dict): 
            module = Module().from_dict(module)
        module.setParentProject(parentproject)
        self.Data[module.ID] = module

    def from_list(self, modulelist: List[Module] = [], parentproject =None):
        self.Data = collections.OrderedDict()
        if not modulelist is None:
            for module in modulelist:
                self.addModule(module, parentproject)
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [m.to_dict() for m in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, modules: dict, parentproject =None):
        self.Data = collections.OrderedDict()
        if not modules is None:
            for key, value in modules.items():
                self.addModule(value, parentproject)
        return self  
    
    def show(self):
        for k, v in self.Data.items():
            print(f'{k}:{v}({v.Name})')
                