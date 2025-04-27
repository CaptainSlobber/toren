from .TorenObject import TorenObject
from .Class import Class
import collections
import json
from typing import List

class Module(TorenObject):


  class PropertName():
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTPROJECT = "ParentProject"
    CLASSES = "Classes"

  class PropertID():
    NAME = "6ef664d9-bbb7-4867-8ab1-fd34f4776b6b"
    DESCRIPTION = "b2c2f6e9-e699-4610-97f6-c46fe6c819c1"
    ID = "b594c4ab-181e-4b4b-9395-e05ca95484f1"
    PARENTPROJECT = "16f4315e-2c49-4d6a-86c8-deccc97ea009" 
    CLASSES = "bfe9f1af-ac7b-4849-a124-ca98b8c642ac"
  
  def __init__(self):
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentProject = None
    self.Classes = []


  def initialize(self, 
                 name: str, 
                 description: str, 
                 id: str,
                 classes: List[Class] = None):
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentProject = None
    self.Classes = self.setClasses(classes)
    return self

  def setClasses(self, classes):
    return self.setClassesFromList(classes)
  
  def setClassesFromList(self, classes):
    _classes = collections.OrderedDict()
    if not classes is None:
      for _class in classes:
        if isinstance(_class, dict): _class = Class().from_dict(_class)
        _class.setParentModule(self)
        _classes[_class.ID] = _class
    return _classes

  def setParentProject(self, parentProject):
    self.ParentProject = parentProject

  def getParentProject(self):
    return self.ParentProject



  def getID(self):
    return self.ID

  def setID(self, id):
    self.ID = id

  def getName(self):
    return self.Name

  def setName(self, name):
    self.Name = name

  def getDescription(self):
    return self.Description

  def setDescription(self, description):
    self.Description = description

  def to_json(self):
    _module_json = json.dumps(self.to_dict())
    return _module_json

  def from_json(self, jsonString):
    _module = json.loads(jsonString)
    self.from_dict(_module)
    return self
  
  def to_dict(self):
    _module = {}
    _module[self.PropertName.NAME] = self.Name
    _module[self.PropertName.DESCRIPTION] = self.Description
    _module[self.PropertName.ID]  = self.ID
    _module[self.PropertName.CLASSES] = [c.to_dict() for c in list(self.Classes.values())]

    return _module
  
  def from_dict(self, module):
    self.Name= str(module[self.PropertName.NAME])
    self.Description = str(module[self.PropertName.DESCRIPTION])
    self.ID = str(module[self.PropertName.ID])
    self.Classes = self.setClasses(module[self.PropertName.CLASSES])
    return self