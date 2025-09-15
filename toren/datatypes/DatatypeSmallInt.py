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

  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
  
  def SQLite_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "BLOB"
    else:
      return "SMALLINT" # https://www.sqlite.org/datatype3.html
  
  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
  
  def PostgreSQL_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "BYTEA"
    else:
      return f"SMALLINT"
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
    
  def Oracle_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "BLOB"
    else:
      return f"SMALLINT"
  
  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
    
  def MicrosoftSQL_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "VARBINARY(MAX)"
    else:
      # https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql-server-data-type-mappings
      return f"SMALLINT"
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"

  ##########################################################################
  # Python methods
  ##########################################################################
  
  def Python_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"npt.NDArray[np.int16]" #np.array/np.ndarray
    else:
      return "int"
  
  def Python_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["import numpy as np", "import numpy.typing as npt"]
    else:
      return []
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.zeros({str(self.Dimensinality)}, dtype=np.int16)"
    else:
      if self.hasDefaultValue():
          return f"{self.DefaultValue}"
      return "0"
    
  ##########################################################################
  # C# methods
  ##########################################################################
  def CSharp_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      commas = ","*(len(self.Dimensinality)-1)  
      return f"int16[{commas}]" #multidimensional array
    else:
      return "int16"
  
  def CSharp_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["using System;"] # Consider: System.Numerics.Vectors
    else:
      return []
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"new int16[{','.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
          return f"{self.DefaultValue}"
      return "0"
    
  ##########################################################################
  # Java methods
  ##########################################################################
  
  def Java_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      brackets = "[]"*(len(self.Dimensinality)) 
      return f"short{brackets}" #multidimensional array
    else:
      return "short"
  
  def Java_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return []
    else:
      return []
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"new short[{']['.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
          return f"{self.DefaultValue}" 
      return "0" 