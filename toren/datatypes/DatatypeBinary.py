from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeBinary(Datatype):

  class PropertName(Datatype.PropertName):
    SIZELIMITKB = "SizeLimitKB"

  class PropertID(Datatype.PropertID):
    SIZELIMITKB = "80e88ec5-37ae-4ff0-81ac-2ada6a0fb2dc"
  
  def getType(self):
    return "toren.datatypes.DatatypeBinary"
  
  def __init__(self):
    super().__init__()
    self.Type = self.getType()


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 foreignKey: ForeignKey=None,
                 sizeLimitkb: int = 1024):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 foreignKey=foreignKey)
    self.Type = self.getType()
    self.SizeLimitkb = sizeLimitkb
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.SizeLimitkb = str(datatype[self.PropertName.SIZELIMITKB])
    self.Type = self.getType()
    return self

  def to_dict(self):
    _datatype = super().to_dict()
    _datatype[self.PropertName.SIZELIMITKB] = self.SizeLimitkb
    return _datatype
  
  def Python(self, *args) -> str:
    return "bytearray"
  
  def Python_Dependencies(self) -> list:
    return [""]
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "bytearray()"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"bytearray({self.DefaultValue})"
    return default_value
  
  def CSharp(self, *args) -> str:
    # TODO: Implement length
    return "byte[]"
  
  def CSharp_Dependencies(self) -> list:
    return [""]
  
  def CSharp_DefaultValue(self, *args) -> str:
    default_value = "new byte[] {}"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"new byte[] {{{self.DefaultValue}}}"
    return default_value