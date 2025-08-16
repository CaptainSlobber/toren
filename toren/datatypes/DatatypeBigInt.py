from .Datatype import Datatype
from .ForeignKey import ForeignKey
from .DatatypeNumeric import DatatypeNumeric
import math
import collections

class DatatypeBigInt(DatatypeNumeric):

  class PropertName(DatatypeNumeric.PropertName):
    pass

  class PropertID(DatatypeNumeric.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeBigInt"
  
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
    _datatypeString = super().to_dict()
    return _datatypeString
  
  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
  
  def SQLite_Type(self, *args):
    if self.hasHigherDimensionality():
      return "BLOB"
    else:
      return "BIGINT"
  
  def SQLite_DefaultValue(self, *args):
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
  
  def PostgreSQL_Type(self, *args):
    if self.hasHigherDimensionality():
      return "BYTEA"
    else:
      return "BIGINT"
  
  def PostgreSQL_DefaultValue(self, *args):
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
    
  def Oracle_Type(self, *args):
    if self.hasHigherDimensionality():
      return "BLOB"
    else:
      return "BIGINT"
  
  def Oracle_DefaultValue(self, *args):
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
    
  def MicrosoftSQL_Type(self, *args):
    if self.hasHigherDimensionality():
      return "VARBINARY(MAX)"
    else:
      return "BIGINT"
  
  def MicrosoftSQL_DefaultValue(self, *args):
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"

  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################
  
  def Python_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"npt.NDArray[np.int64]" #np.array/np.ndarray
    else:
      return "int"
  
  def Python_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["import numpy as np", "import numpy.typing as npt"]
    else:
      return [""]
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.zeros({str(self.Dimensinality)}, dtype=np.int64)"
    else:
      default_value = "0"
      if self.hasDefaultValue():
        default_value = f"{str(int(self.DefaultValue))}"
      return default_value
    
  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################
    
  def CSharp_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      commas = ","*(len(self.Dimensinality)-1)  
      return f"long[{commas}]" #multidimensional array
    else:
      return "long"
  
  def CSharp_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["using System;"] # Consider: System.Numerics.Vectors
    else:
      return [""]
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"new long[{','.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"