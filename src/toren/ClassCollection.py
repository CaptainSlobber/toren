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


    def dedict_list(self, classlist: List[Class] = []):
        _classlist = []

        for class_ in classlist:
            if isinstance(class_, dict): 
                class_ = Class().from_dict(class_)

            _classlist.append(class_)
        return _classlist
    
    def class_list_search_inheritence(self, sorted, p, rem):
        if (len(rem) == 0):
            return sorted
        elif (len(p) == 0):
            _p = []
            _rem = []
            for c in rem:
                if c.InheritsFromID is None:
                    _p.append(c)
                else:
                    _rem.append(c)
            sorted = sorted + _p
            sorted = self.class_list_search_inheritence(sorted ,_p, _rem)
            return sorted
        else:
            _p = []
            _rem = []
            for c in rem:
                inflg = False
                for _c in p:
                    if c.InheritsFromID == _c.ID:
                        inflg = True
                if inflg:
                    _p.append(c)
                else:
                    _rem.append(c)
            sorted = sorted + _p
            sorted = self.class_list_search_inheritence(sorted ,_p, _rem)
            return sorted



    def sort_class_list(self, classlist: List[Class] = []):

        classlist  = self.dedict_list(classlist)
        _classlist = self.class_list_search_inheritence([],[], classlist)
        return _classlist
        
    def from_list(self, classlist: List[Class] = [], parentmodule =None):
        self.Data = collections.OrderedDict()
        if not classlist is None:
            classlist = self.sort_class_list(classlist=classlist)
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
        classlist = []
        if not classes is None:
            for key, value in classes.items():
                classlist.append(value)
        return self.from_list(classlist, parentmodule=parentmodule)  
                