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
                 dimensionality: list = [],
                 foreignKey: ForeignKey=None):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 dimensionality=dimensionality,
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
  
  def Python(self, *args) -> str:
    return "uuid.UUID"
  
  def Python_Dependencies(self) -> list:
    return ['import uuid']
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "uuid.uuid4()"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"uuid.UUID('{self.DefaultValue}')"
    return default_value
  