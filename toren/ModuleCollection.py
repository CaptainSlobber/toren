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

    
    def addModule(self, module, modulecollection, parentproject):
        if isinstance(module, dict): 
            module = Module().from_dict(module)
        module.setParentProject(parentproject)
        modulecollection[module.ID] = module
        return modulecollection

    def from_list(self, modulelist: List[Module] = [], parentproject =None):
        _modules = collections.OrderedDict()
        if not modulelist is None:
            for module in modulelist:
                _modules = self.addModule(module, _modules, parentproject)
        self.Data = _modules
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [m.to_dict() for m in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, modules: dict, parentproject =None):
        _modules = collections.OrderedDict()
        if not modules is None:
            for key, value in modules.items():
                _modules = self.addModule(value, _modules, parentproject)
        self.Data = _modules
        return self  
                