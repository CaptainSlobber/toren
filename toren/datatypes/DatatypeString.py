from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections
import base64

class DatatypeString(Datatype):

  class PropertName(Datatype.PropertName):
    MAXLENGTH = "MaxLength"
    REGEX = "Regex"

  class PropertID(Datatype.PropertID):
    MAXLENGTH = "cef913a1-4297-4834-9337-a337ec10ce80"
    REGEX = "9aa7e590-f7e1-4b91-a5dd-e257760c46f8"
  
  def getType(self):
    return "toren.datatypes.DatatypeString"
  
  def __init__(self):
    super().__init__()
    self.Type = self.getType()
    self.MaxLength = 32


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 foreignKey: ForeignKey=None,
                 maxlength: int = 32,
                 regex: str = ""):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 foreignKey=foreignKey)
    self.Type = self.getType()
    self.MaxLength = maxlength
    self.Regex = regex
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.Type = self.getType()
    self.MaxLength = bool(datatype[self.PropertName.MAXLENGTH])
    self.Regex = bool(datatype[self.PropertName.MAXLENGTH]) # Handle Escape
    return self

  def to_dict(self):
    _datatypeString = super().to_dict()
    _datatypeString[self.PropertName.MAXLENGTH] = self.MaxLength
    _datatypeString[self.PropertName.REGEX] = self.Regex # Handle Escape
    return _datatypeString
  

  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
   
  def SQLite_Type(self, *args) -> str:
    return f"NVARCHAR({int(self.MaxLength)})" # UTF-16
  
  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._DefaultValueSingleQuote()
    return self._SingleQuote("")

  def PostgreSQL_Type(self, *args) -> str:
    return f"VARCHAR({int(self.MaxLength)})" # TEXT
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._DefaultValueSingleQuote()
    return self._SingleQuote("")
    
  def Oracle_Type(self, *args) -> str:
     return f"NVARCHAR2({int(self.MaxLength)})" # UTF-16
  
  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._DefaultValueSingleQuote()
    return self._SingleQuote("")
  
  def MicrosoftSQL_Type(self, *args) -> str:
    return f"NVARCHAR({int(self.MaxLength)})" # UTF-16
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._DefaultValueSingleQuote()
    return self._SingleQuote("")


  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "str"
  
  def Python_Dependencies(self) -> list:
    return [] # import re
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._DefaultValueDoubleQuote()
    return self._DoubleQuote("")

  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################

  def CSharp_Type(self, *args) -> str:
    return "string"
  
  def CSharp_Dependencies(self) -> list:
    return ["using System;"] 
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return self._DefaultValueDoubleQuote()
    return "String.Empty"