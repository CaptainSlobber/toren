from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeBoolean(Datatype):

  class PropertName(Datatype.PropertName):
    pass

  class PropertID(Datatype.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeBoolean"
  
  def __init__(self):
    super().__init__()
    self.Type = self.getType()


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 foreignKey: ForeignKey=None):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 foreignKey=foreignKey)
    self.Type = self.getType()
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.Type = self.getType()
    return self

  def to_dict(self):
    _datatype = super().to_dict()
    return _datatype
  
  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
   
  def SQLite_Type(self, *args):
    return "BOOLEAN"
  
  def SQLite_DefaultValue(self, *args):
    return "0"
  
  def PostgreSQL_Type(self, *args):
    return "BOOLEAN"
  
  def PostgreSQL_DefaultValue(self, *args):
    return "FALSE" # "0"
    
  def Oracle_Type(self, *args):
     return "NUMBER(1)"
  
  def Oracle_DefaultValue(self, *args):
    return "0"
    
  def MicrosoftSQL_Type(self, *args):
    return "BIT"
  
  def MicrosoftSQL_DefaultValue(self, *args):
    return "0"
  
  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "bool"
  
  def Python_Dependencies(self) -> list:
    return []
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "False"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"{self.DefaultValue.capitalize()}"
    return default_value
  

  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################
  
  def CSharp_Type(self, *args) -> str:
    return "bool"
  
  def CSharp_Dependencies(self) -> list:
    return [""]
  
  def CSharp_DefaultValue(self, *args) -> str:
    default_value = "false"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"{self.DefaultValue.lower()}"
    return default_value