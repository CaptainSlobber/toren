from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeString(Datatype):

  class PropertName(Datatype.PropertName):
    MAXLENGTH = "MaxLength"

  class PropertID(Datatype.PropertID):
    MAXLENGTH = "cef913a1-4297-4834-9337-a337ec10ce80"
  
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
                 dimensionality: list = [],
                 foreignKey: ForeignKey=None,
                 maxlength: int = 32):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 dimensionality=dimensionality,
                 foreignKey=foreignKey)
    self.Type = self.getType()
    self.MaxLength = maxlength
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.Type = self.getType()
    self.MaxLength = bool(datatype[self.PropertName.MAXLENGTH])
    return self

  def to_dict(self):
    _datatypeString = super().to_dict()
    _datatypeString[self.PropertName.MAXLENGTH] = self.MaxLength
    return _datatypeString
  
  def Python(self, *args) -> str:
    return "str"
  
  def Python_Dependencies(self) -> list:
    return []
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "\"\""
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"\"{self.DefaultValue}\""
    return default_value