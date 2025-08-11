from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeUUID(Datatype):

  class PropertName(Datatype.PropertName):
    pass

  class PropertID(Datatype.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeUUID"
  
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
  
  def Python_Type(self, *args) -> str:
    return "uuid.UUID"
  
  def Python_Dependencies(self) -> list:
    return ['import uuid']
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "uuid.uuid4()"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"uuid.UUID('{self.DefaultValue}')"
    return default_value
  
  def CSharp_Type(self, *args) -> str:
    return "System.Guid"
  
  def CSharp_Dependencies(self) -> list:
    return ["using System;"] 
  
  def CSharp_DefaultValue(self, *args) -> str:
    default_value = 'System.Guid.NewGuid()'
    if self.DefaultValue:
      if len(self.DefaultValue) > 0: # TODO: Validate if string is a valid UUID
        default_value = f'System.Guid.NewGuid("{self.DefaultValue}")'
    return default_value