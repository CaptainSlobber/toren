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
   
  def SQLite_Type(self, *args) -> str:
    return "BOOLEAN"
  
  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue.capitalize() == 'True'))}"
    return "0"

  
  def PostgreSQL_Type(self, *args) -> str:
    return "BOOLEAN"
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"{self.DefaultValue.upper()}"
    return "FALSE" # "0"
    
  def Oracle_Type(self, *args) -> str:
     return "NUMBER(1)"
  
  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"{str(int(self.DefaultValue.capitalize() == 'True'))}"
    return "0"
    
  def MicrosoftSQL_Type(self, *args) -> str:
    return "BIT"
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"{str(int(self.DefaultValue.capitalize() == 'True'))}"
    return "0"
  
  ##########################################################################
  # Python methods
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "bool"
  
  def Python_Dependencies(self) -> list:
    return []
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"{self.DefaultValue.capitalize()}"
    return "False"
  

  ##########################################################################
  # C# methods
  ##########################################################################
  def CSharp_Type(self, *args) -> str:
    return "bool"
  
  def CSharp_Dependencies(self) -> list:
    return []
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"{self.DefaultValue.lower()}"
    return "false"
  
  def Python_to_Oracle(self, *args) -> str:
    return f"int({args[0]})"

  def Python_to_MicrosoftSQL(self, *args) -> str:
    return f"int({args[0]})"
  
  def Python_to_PostgreSQL(self, *args) -> str:
    return f"int({args[0]})"
  
  def Python_to_SQLite(self, *args) -> str:
    return f"int({args[0]})"

  def Python_from_Oracle(self, *args) -> str:
    return f"bool({args[0]})"
   
  def Python_from_MicrosoftSQL(self, *args) -> str:
    return f"bool({args[0]})"
  
  def Python_from_PostgreSQL(self, *args) -> str:
    return f"bool({args[0]})"
  
  def Python_from_SQLite(self, *args) -> str:
    return f"bool({args[0]})"
  

  ##########################################################################
  # Java methods
  ##########################################################################
  def Java_Type(self, *args) -> str:
    return "Boolean" #"boolean"
  
  def Java_Dependencies(self) -> list:
    return []
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"{self.DefaultValue.lower()}"
    return "false"
