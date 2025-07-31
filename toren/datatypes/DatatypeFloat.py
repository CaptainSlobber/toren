from .Datatype import Datatype
from .ForeignKey import ForeignKey
from .DatatypeNumeric import DatatypeNumeric
import collections

class DatatypeFloat(DatatypeNumeric):

  class PropertName(DatatypeNumeric.PropertName):
    pass

  class PropertID(DatatypeNumeric.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeFloat"
  
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
                 foreignKey=foreignKey,
                 minimum=minimum,
                 maximum=maximum)
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
    if len(self.Dimensinality) > 0:
      return f"npt.NDArray[np.float32]" #np.array/np.ndarray
    else:
      return "float"
  
  def Python_Dependencies(self) -> list:
    if len(self.Dimensinality) > 0:
      return ["import numpy as np", "import numpy.typing as npt"]
    else:
      return [""]
  
  def Python_DefaultValue(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      return f"np.zeros({str(self.Dimensinality)}, dtype=np.float32)"
    else:
      default_value = "0.0" 
      if self.DefaultValue:
        if len(self.DefaultValue) > 0:
          default_value = f"float({self.DefaultValue})"
      return default_value
    
  def CSharp(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      commas = ","*(len(self.Dimensinality)-1)  
      return f"float[{commas}]" #multidimensional array
    else:
      return "float"
  
  def CSharp_Dependencies(self) -> list:
    if len(self.Dimensinality) > 0:
      return ["using System;"] # Consider: System.Numerics.Vectors
    else:
      return [""]
  
  def CSharp_DefaultValue(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      return f"new float[{','.join(self.Dimensinality)}]"
    else:
      default_value = "0.0f"
      if self.DefaultValue:
        if len(self.DefaultValue) > 0:
          default_value = f"{self.DefaultValue}f"
      return default_value