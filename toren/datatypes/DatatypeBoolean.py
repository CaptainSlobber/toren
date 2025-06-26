from .Datatype import Datatype
import collections

class DatatypeBoolean(Datatype):
  
  def getType(self):
    return "toren.datatypes.DatatypeBoolean"
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentModule = None
    self.IsPrimaryKey = False
    self.IsUnique = False
    self.DefaultValue = ""
    self.Dimensinality = None

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