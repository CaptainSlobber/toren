from .Datatype import Datatype
from .ForeignKey import ForeignKey
from .DatatypeNumeric import DatatypeNumeric
import math
import collections

class DatatypeSmallInt(DatatypeNumeric):

  class PropertName(DatatypeNumeric.PropertName):
    pass

  class PropertID(DatatypeNumeric.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeSmallInt"
  
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
                 minimum=math.floor(minimum),
                 maximum=math.floor(maximum))
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
      return f"npt.NDArray[np.int16]" #np.array/np.ndarray
    else:
      return "int"
  
  def Python_Dependencies(self) -> list:
    if len(self.Dimensinality) > 0:
      return ["import numpy as np", "import numpy.typing as npt"]
    else:
      return [""]
  
  def Python_DefaultValue(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      return f"np.zeros({str(self.Dimensinality)}, dtype=np.int16)"
    else:
      default_value = "0"
      if self.DefaultValue:
        if len(self.DefaultValue) > 0:
          default_value = f"{self.DefaultValue}"
      return default_value

  def CSharp(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      commas = ","*(len(self.Dimensinality)-1)  
      return f"int16[{commas}]" #multidimensional array
    else:
      return "int16"
  
  def CSharp_Dependencies(self) -> list:
    if len(self.Dimensinality) > 0:
      return ["using System;"] # Consider: System.Numerics.Vectors
    else:
      return [""]
  
  def CSharp_DefaultValue(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      return f"new int16[{','.join(self.Dimensinality)}]"
    else:
      default_value = "0"
      if self.DefaultValue:
        if len(self.DefaultValue) > 0:
          default_value = f"{self.DefaultValue}"
      return default_value