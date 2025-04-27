from ..TorenObject import TorenObject
import collections
import json

class Datatype(TorenObject):


  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTMODULE = "ParentModule"
    ISPRIMARYKEY = "IsPrimaryKey"
    ISUNIQUE = "IsUnique"
    DEFAULTVALUE = "DefaultValue"


  class PropertID():
    TYPE = ""
    NAME = ""
    DESCRIPTION = ""
    ID = ""
    PARENTMODULE = ""
    ISPRIMARYKEY = ""
    ISUNIQUE = ""
    DEFAULTVALUE = ""

  def getType(self):
    return "toren.datatypes.Datatype"
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentModule = None
    self.IsPrimaryKey = False
    self.IsUnique = False
    self.DefaultValue = ""


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = ""):
    self.Type = self.getType()
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentModule = None
    self.IsPrimaryKey = isprimarykey
    self.IsUnique = isunique
    self.DefaultValue = defaultvalue
    return self
  
  def setParentClass(self, parentclass):
    self.ParentClass = parentclass


  def from_dict(self, datatype):
    #self.Type = str(datatype[self.PropertName.TYPE])
    self.Name= str(datatype[self.PropertName.NAME])
    self.Description = str(datatype[self.PropertName.DESCRIPTION]) 
    self.ID = str(datatype[self.PropertName.ID])
    self.IsPrimaryKey = bool(datatype[self.PropertName.ISPRIMARYKEY])
    self.IsUnique = bool(datatype[self.PropertName.ISUNIQUE])
    return self

  def to_dict(self):
    _datatype = {}
    _datatype[self.PropertName.TYPE] = self.Type
    _datatype[self.PropertName.NAME] = self.Name
    _datatype[self.PropertName.DESCRIPTION] = self.Description
    _datatype[self.PropertName.ID] = self.ID
    _datatype[self.PropertName.ISPRIMARYKEY] = self.IsPrimaryKey
    _datatype[self.PropertName.ISUNIQUE] = self.IsUnique
    return _datatype
  
  def to_json(self):
    _datatype_json = json.dumps(self.to_dict())
    return _datatype_json

  def from_json(self, jsonString):
    _datatype = json.loads(jsonString)
    self.from_dict(_datatype)
    return self