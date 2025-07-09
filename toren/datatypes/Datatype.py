from ..TorenObject import TorenObject
from .ForeignKey import ForeignKey
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
    DIMENSIONALITY = "Dimensionality"
    FOREIGNKEY = "ForeignKey"


  class PropertID():
    TYPE = "3b44d998-ef93-4d3c-b01f-fea888f7ad8d"
    NAME = "4310715d-f631-44f4-b0b8-8e56c90547d9"
    DESCRIPTION = "e75bc526-8ae7-4f23-943a-73bc9448edc4"
    ID = "a066d0fc-392f-44ea-bbd6-da6e71bf7002"
    PARENTMODULE = "ea08aad9-b34b-4990-9b85-572841672f62"
    ISPRIMARYKEY = "ea0ebb8c-57e7-4c36-b834-132dd1329690"
    ISUNIQUE = "01a9e2b8-3a64-4832-bb01-ce05120fb9f8"
    DEFAULTVALUE = "e9009d06-73ed-4e73-a5bb-4836badf4037"
    DIMENSIONALITY = "aa74f0c8-5d31-4622-9844-c0739afb94e5"
    FOREIGNKEY = "f3553d5e-f65f-4a70-b45f-1db6ccb714b1"

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
    self.Dimensinality = []
    self.ForeignKey = None


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 dimensionality: list = [],
                 foreignKey: ForeignKey=None):
    self.Type = self.getType()
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentModule = None
    self.ForeignKey = None
    self.IsPrimaryKey = isprimarykey
    self.IsUnique = isunique
    self.DefaultValue = defaultvalue
    self.Dimensinality = dimensionality
    self.ForeignKey = foreignKey
    return self
  
  def setParentClass(self, parentclass):
    self.ParentClass = parentclass
    return self

  def setForeignKey(self, foreignkeypropertyname, foreignkeyclassproperty, foreignkeyclass=None):
    self.ForeignKey = ForeignKey().initialize(foreignkeypropertyname, foreignkeyclassproperty, foreignkeyclass)
    return self

  def from_dict(self, datatype):
    self.Type = self.getType()
    self.Name= str(datatype[self.PropertName.NAME])
    self.Description = str(datatype[self.PropertName.DESCRIPTION]) 
    self.ID = str(datatype[self.PropertName.ID])
    self.IsPrimaryKey = bool(datatype[self.PropertName.ISPRIMARYKEY])
    self.IsUnique = bool(datatype[self.PropertName.ISUNIQUE])
    self.DefaultValue = str(datatype[self.PropertName.DEFAULTVALUE])
    self.Dimensinality = datatype[self.PropertName.DIMENSIONALITY]

    if self.PropertName.FOREIGNKEY in datatype: 
      self.ForeignKey = ForeignKey().from_dict(datatype[self.PropertName.FOREIGNKEY])
    return self

  def to_dict(self):
    _datatype = {}
    _datatype[self.PropertName.TYPE] = self.Type
    _datatype[self.PropertName.NAME] = self.Name
    _datatype[self.PropertName.DESCRIPTION] = self.Description
    _datatype[self.PropertName.ID] = self.ID
    _datatype[self.PropertName.ISPRIMARYKEY] = self.IsPrimaryKey
    _datatype[self.PropertName.ISUNIQUE] = self.IsUnique
    _datatype[self.PropertName.DEFAULTVALUE] = self.DefaultValue
    _datatype[self.PropertName.DIMENSIONALITY] = self.Dimensinality
    if self.ForeignKey is not None: 
      _datatype[self.PropertName.FOREIGNKEY] = self.ForeignKey.to_dict()
    return _datatype
  
  def to_json(self):
    _datatype_json = json.dumps(self.to_dict())
    return _datatype_json

  def from_json(self, jsonString):
    _datatype = json.loads(jsonString)
    self.from_dict(_datatype)
    return self
  
  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################
  def Python(self, *args) -> str:
    raise NotImplementedError
  
  def Python_Dependencies(self) -> list:
    return NotImplementedError
  
  def Python_DefaultValue(self, *args) -> str:
    return NotImplementedError
  
  def Python_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Python_to_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def Python_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Python_from_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_from_SQLite(self, *args) -> str:
    raise NotImplementedError

  ##########################################################################
  # Java methods for converting to and from various database types
  ##########################################################################
  def Java(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def Java_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Java_from_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_from_SQLite(self, *args) -> str:
    raise NotImplementedError
  
  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################
  def CSharp(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def CSharp_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_from_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_from_SQLite(self, *args) -> str:
    raise NotImplementedError

  #########################################################################
  # Go methods for converting to and from various database types
  ##########################################################################
  def Go(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def Go_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Go_from_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_from_SQLite(self, *args) -> str:
    raise NotImplementedError

  #########################################################################
  # JavaScript methods for converting to and from various database types
  ##########################################################################
  def JavaScript(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def JavaScript_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_from_MicrosftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_from_SQLite(self, *args) -> str:
    raise NotImplementedError
  

