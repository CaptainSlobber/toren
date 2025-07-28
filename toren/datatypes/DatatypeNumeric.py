from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeNumeric(Datatype):

  class PropertName(Datatype.PropertName):
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"

  class PropertID(Datatype.PropertID):
    MINIMUM = "17412aaa-bc9c-4d17-9467-c84035a2d15a"
    MAXIMUM = "bcecdbd1-6b6e-4de3-9790-b7f7e9ea0de1"
  
  def getType(self):
    return "toren.datatypes.DatatypeNumeric"
  
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
                 foreignKey: ForeignKey=None,
                 minimum: float = 0.0,
                 maximum: float = 100.0):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 dimensionality=dimensionality,
                 foreignKey=foreignKey)
    self.Minimumn = minimum
    self.Maximum = maximum
    self.Type = self.getType()
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.Minimumn = float(datatype[self.PropertName.MINIMUM])
    self.Maximum = float(datatype[self.PropertName.MAXIMUM])
    self.Type = self.getType()
    return self

  def to_dict(self):
    _datatype = super().to_dict()
    _datatype[self.PropertName.MINIMUM] = self.Minimumn
    _datatype[self.PropertName.MAXIMUM] = self.Maximum
    return _datatype
  
  def Python(self, *args) -> str:
    return "float"
  
  def Python_Dependencies(self) -> list:
    return [""]
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "0.0" 
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"float({self.DefaultValue})"
    return default_value