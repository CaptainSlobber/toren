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
    
    def setInheritence(self):
        for classid, _class in self.Data.items():
            if _class.InheritsFromID is not None:
                _class.InheritsFrom = self.Data[_class.InheritsFromID]
            else:
                _class.InheritsFrom = None

    def getItem(self, id):
        if id in self.Data:
            return self.Data[id]

        return None
    
    def removeClass(self, key):
        if key in self.Data:
            del self.Data[key]

    def addCollection(self, collection):
        _colletion = self.Data

        for k,v in collection.Data.items():
            _colletion[k] = v

        self.Data = _colletion
        return self   


    def show(self):
        for k, v in self.Data.items():
            print(f'{k}:{v}({v.Name})')

    def addClass(self, _class, parentmodule):
        if isinstance(_class, dict): 
            _class = Class().from_dict(_class)
        _class.setParentModule(parentmodule)

        if _class.InheritsFromID is not None:
            if _class.InheritsFromID in self.Data:
                _class.InheritsFrom = self.Data[_class.InheritsFromID]
        self.Data[_class.ID] = _class

    def from_list(self, classlist: List[Class] = [], parentmodule =None):
        self.Data = collections.OrderedDict()
        if not classlist is None:
            for _class in classlist:
                self.addClass(_class, parentmodule)
        self.setInheritence()
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [c.to_dict() for c in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, classes: dict, parentmodule =None):
        self.Data = collections.OrderedDict()
        if not classes is None:
            for key, value in classes.items():
                self.addClass(value, parentmodule)

        self.setInheritence()
        return self  
                