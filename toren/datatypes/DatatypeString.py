from .Datatype import Datatype
import collections

class DatatypeString(Datatype):

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTMODULE = "ParentModule"
    ISPRIMARYKEY = "IsPrimaryKey"
    ISUNIQUE = "IsUnique"
    DEFAULTVALUE = "DefaultValue"
    MAXLENGTH = "MaxLength"
  
  def getType(self):
    return "toren.datatypes.DatatypeString"
  
  def __init__(self):
    super().__init__()
    self.Type = self.getType()
    # self.Name = ""
    # self.Description = ""
    # self.ID = ""
    # self.ParentModule = None
    # self.IsPrimaryKey = False
    # self.IsUnique = False
    # self.DefaultValue = ""
    self.MaxLength = 32


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 maxlength: int = 32):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue)
    self.Type = self.getType()
    self.MaxLength = maxlength
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.MaxLength = bool(datatype[self.PropertName.MAXLENGTH])
    return self

  def to_dict(self):
    _datatypeString = super().to_dict()
    _datatypeString[self.PropertName.MAXLENGTH] = self.MaxLength
    return _datatypeString