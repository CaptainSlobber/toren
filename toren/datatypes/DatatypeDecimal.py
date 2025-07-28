from .Datatype import Datatype
from .ForeignKey import ForeignKey
from .DatatypeNumeric import DatatypeNumeric
import collections

class DatatypeDecimal(DatatypeNumeric):

  class PropertName(DatatypeNumeric.PropertName):
    PRECISION = "Precision"
    SCALE = "Scale"

  class PropertID(DatatypeNumeric.PropertID):
    PRECISION = "2a43476d-5856-4b6b-92dd-62ae95a8844f"
    SCALE = "2a43476d-5856-4b6b-92dd-62ae95a8844f"
  
  
  def getType(self):
    return "toren.datatypes.DatatypeDecimal"
  
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
                 maximum: float = 100.0,
                 precision: int = 2,
                 scale: int = 2):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 dimensionality=dimensionality,
                 foreignKey=foreignKey,
                 minimum=minimum,
                 maximum=maximum)
  
    # precision (p) is the maximum number of all digits (both sides of the decimal point),
    self.Precision = precision
    # scale (s) is the maximum number of digits after the decimal point
    self.Scale = scale
    self.Type = self.getType()
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.Precision = float(datatype[self.PropertName.PRECISION])
    self.Scale = float(datatype[self.PropertName.SCALE])
    self.Type = self.getType()
    return self

  def to_dict(self):
    _datatype = super().to_dict()
    _datatype[self.PropertName.PRECISION] = self.Precision
    _datatype[self.PropertName.SCALE] = self.Scale
    return _datatype
  
  def Python(self, *args) -> str:
    return "Decimal"
  
  def Python_Dependencies(self) -> list:
    return ['from decimal import Decimal']
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "Decimal(0.0)"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"Decimal('{self.DefaultValue}')"
    return default_value
  