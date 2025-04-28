from .Class import Class

import collections
import json
from typing import List


class ClassCollection():

    def getType(self):
        return "toren.ClassCollection"
    
    def __init__(self):
        self.Data = collections.OrderedDict()

    
    def initialize(self, classlist: List[Class] = [], parentmodule = None):
        self.from_list(classlist, parentmodule)
        return self

    
    def addClass(self, _class, classcollection, parentmodule):
        if isinstance(_class, dict): 
            _class = Class().from_dict(_class)
        _class.setParentModule(parentmodule)
        classcollection[_class.ID] = _class
        return classcollection

    def from_list(self, classlist: List[Class] = [], parentmodule =None):
        _classes = collections.OrderedDict()
        if not classlist is None:
            for _class in classlist:
                _classes = self.addClass(_class, _classes, parentmodule)
        self.Data = _classes
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [c.to_dict() for c in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, classes: dict, parentmodule =None):
        _classes = collections.OrderedDict()
        if not classes is None:
            for key, value in classes.items():
                _classes = self.addClass(value, _classes, parentmodule)
        self.Data = _classes
        return self  
                