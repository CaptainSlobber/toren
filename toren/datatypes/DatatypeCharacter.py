from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeCharacter(Datatype):

  class PropertName(Datatype.PropertName):
    pass

  class PropertID(Datatype.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeCharacter"
  
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
    
    if len(defaultvalue) > 1: defaultvalue = defaultvalue[0] # First character only
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

  def SQLite_Type(self, *args) -> str:
    return "TEXT"  # SQLite uses TEXT for string/character data

  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"\"{self.DefaultValue[0]}\""
    return "\"\""

  def PostgreSQL_Type(self, *args) -> str:
    return "CHAR(1)"  # Single character

  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"\"{self.DefaultValue[0]}\""
    return "\"\""

  def Oracle_Type(self, *args) -> str:
    return "CHAR(1)"

  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"\"{self.DefaultValue[0]}\""
    return "\"\""

  def MicrosoftSQL_Type(self, *args) -> str:
    return "CHAR(1)"

  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"\"{self.DefaultValue[0]}\""
    return "\"\""
  
  ##########################################################################
  # Python methods
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "str"
  
  def Python_Dependencies(self) -> list:
    return []
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return f"\"{self.DefaultValue[0]}\"" # First character only
    return "\"\""
  
  def Python_to_Oracle(self, *args) -> str:
    return f"{args[0]}[0]"

  def Python_to_MicrosoftSQL(self, *args) -> str:
    return f"{args[0]}[0]"
  
  def Python_to_PostgreSQL(self, *args) -> str:
    return f"{args[0]}[0]"
  
  def Python_to_SQLite(self, *args) -> str:
    return f"{args[0]}[0]"

  def Python_from_Oracle(self, *args) -> str:
    return f"str({args[0]})[0]"
  
  def Python_from_MicrosoftSQL(self, *args) -> str:
    return f"str({args[0]})[0]"
  
  def Python_from_PostgreSQL(self, *args) -> str:
    return f"str({args[0]})[0]"
  
  def Python_from_SQLite(self, *args) -> str:
    return f"str({args[0]})[0]"
  
  ##########################################################################
  # C# methods
  ##########################################################################
  
  def CSharp_Type(self, *args) -> str:
    return "char[]"
  
  def CSharp_Dependencies(self) -> list:
    return []
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        #return f"new char[1] {{{self.DefaultValue}}}"
        return f"['{self.DefaultValue}']"
    return "new char[1]"
  
  ##########################################################################
  # Java methods
  ##########################################################################
  
  def Java_Type(self, *args) -> str:
    return "char[]"
  
  def Java_Dependencies(self) -> list:
    return []
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return f'new String("{self.DefaultValue}").toCharArray()'
    return "new char[1]"