from .TorenObject import TorenObject
from .Class import Class
from .ClassCollection import ClassCollection
import collections
import json
from typing import List

class Module(TorenObject):


  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTPROJECT = "ParentProject"
    CLASSES = "Classes"
    

  class PropertID():
    TYPE = "7c5e3037-ed1d-4ede-b7f0-716382976ea6"
    NAME = "6ef664d9-bbb7-4867-8ab1-fd34f4776b6b"
    DESCRIPTION = "b2c2f6e9-e699-4610-97f6-c46fe6c819c1"
    ID = "b594c4ab-181e-4b4b-9395-e05ca95484f1"
    PARENTPROJECT = "16f4315e-2c49-4d6a-86c8-deccc97ea009" 
    CLASSES = "bfe9f1af-ac7b-4849-a124-ca98b8c642ac"
  
  def __init__(self):
    self.Type = "toren.Module"
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentProject = None
    self.Classes = ClassCollection()


  def initialize(self, 
                 name: str, 
                 description: str, 
                 id: str,
                 classes: List[Class] = None):
    self.Type = "toren.Module"
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentProject = None
    self.Classes = ClassCollection().initialize(classes, self)
    return self

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
    _module[self.PropertName.TYPE] = self.Type
    _module[self.PropertName.NAME] = self.Name
    _module[self.PropertName.DESCRIPTION] = self.Description
    _module[self.PropertName.ID]  = self.ID
    _module[self.PropertName.CLASSES] = self.Classes.to_list_of_dict()

    return _module
  
  def from_dict(self, module):
    #self.Type = str(module[self.PropertName.TYPE])
    self.Name = str(module[self.PropertName.NAME])
    self.Description = str(module[self.PropertName.DESCRIPTION])
    self.ID = str(module[self.PropertName.ID])
    self.Classes = ClassCollection().initialize(module[self.PropertName.CLASSES], self)
    return self