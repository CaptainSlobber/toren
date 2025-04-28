from .TorenObject import TorenObject
from .datatypes import *
import collections
import json
from typing import List



class Class(TorenObject):


  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTMODLUE = "ParentModule"
    PROPERTIES = "Properties"

  class PropertID():
    TYPE = "1fefc4f1-a3da-4c55-a5c5-2332e1330a07"
    NAME = "5c44f1d6-45ef-4cf7-848b-efda7e417d56"
    DESCRIPTION = "d72d62ff-2d93-4d82-bc30-37f927501b8b"
    ID = "93037bdc-ccd6-4c06-9473-ab2a39d56d1b"
    PARENTMODLUE = "1ab7f6b9-635c-48ec-929f-3d041e34dcee" 
    PROPERTIES = "b95a7a80-21b8-417f-862c-49365faa94d0"
  
  def __init__(self):
    self.Type = "toren.Class"
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentModule = None
    self.Properties = DatatypeCollection()


  def initialize(self, 
                 name: str, 
                 description: str, 
                 id: str,
                 properties: List[Datatype] = None):
    self.Type = "toren.Class"
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentModule = None
    self.Properties = DatatypeCollection().initialize(properties, self) #self.setProperties(properties)
    return self



  def setParentModule(self, parentModule):
    self.ParentModule = parentModule

  def to_json(self):
    _module_json = json.dumps(self.to_dict())
    return _module_json

  def from_json(self, jsonString):
    _class = json.loads(jsonString)
    self.from_dict(_class)
    return self
  
  def to_dict(self):
    _class = {}
    _class[self.PropertName.TYPE] = self.Type
    _class[self.PropertName.NAME] = self.Name
    _class[self.PropertName.DESCRIPTION] = self.Description
    _class[self.PropertName.ID]  = self.ID
    _class[self.PropertName.PROPERTIES] = self.Properties.to_list_of_dict()

    return _class
  
  def from_dict(self, _class):
    #self.Type = str(_class[self.PropertName.TYPE])
    self.Name = str(_class[self.PropertName.NAME])
    self.Description = str(_class[self.PropertName.DESCRIPTION])
    self.ID = str(_class[self.PropertName.ID])
    self.Properties = DatatypeCollection().initialize(_class[self.PropertName.PROPERTIES], self)
    return self
