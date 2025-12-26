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
  

  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
  
  def SQLite_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "BLOB"
    else:
      return "REAL"
  
  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{self.DefaultValue}"
      return "0.0"
  
  def PostgreSQL_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "BYTEA"
    else:
      return f"DECIMAL({int(self.Precision)}, {int(self.Scale)})"
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{self.DefaultValue}"
      return "0.0"
    
  def Oracle_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "BLOB"
    else:
      return f"DECIMAL({int(self.Precision)}, {int(self.Scale)})"
  
  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{self.DefaultValue}"
      return "0.0"
    
  def MicrosoftSQL_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return "VARBINARY(MAX)"
    else:
      return f"DECIMAL({int(self.Precision)}, {int(self.Scale)})"
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return self.defaultBlob()
    else:
      if self.hasDefaultValue():
        return f"{self.DefaultValue}"
      return "0.0"

  ##########################################################################
  # Python methods
  ##########################################################################
  NPDTYPE = "longdouble"

  def Python_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"npt.NDArray[np.{self.NPDTYPE}]" # Sorta 
    else:
      return "Decimal"
  
  def Python_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["import numpy as np", "import numpy.typing as npt", "import json"]
    else:
      return ['from decimal import Decimal']
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.zeros({str(self.Dimensinality)}, dtype=np.{self.NPDTYPE})" # Kinda 
    else:
      if self.hasDefaultValue():
          return f"Decimal('{self.DefaultValue}')"
      return "Decimal(0.0)"
    
  def Python_to_Oracle(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"json.dumps({args[0]}.tolist()).encode('utf-8')"
    else:
      return f"{args[0]}"

  def Python_to_MicrosoftSQL(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"json.dumps({args[0]}.tolist()).encode('utf-8')"
    else:
      return f"{args[0]}"
  
  def Python_to_PostgreSQL(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"json.dumps({args[0]}.tolist()).encode('utf-8')"
    else:
      return f"{args[0]}"
  
  def Python_to_SQLite(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"json.dumps({args[0]}.tolist()).encode('utf-8')"
    else:
      return f"{args[0]}"

  def Python_from_Oracle(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads({args[0]}.read().decode('utf-8')), dtype=np.{self.NPDTYPE})"
    else:
      return f"Decimal({args[0]})"
  
  def Python_from_MicrosoftSQL(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads({args[0]}.decode('utf-8')), dtype=np.{self.NPDTYPE})"
    else:
      return f"Decimal({args[0]})"
  
  def Python_from_PostgreSQL(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads(bytes({args[0]}).decode('utf-8')), dtype=np.{self.NPDTYPE})"
    else:
      return f"Decimal({args[0]})"
  
  def Python_from_SQLite(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads({args[0]}.decode('utf-8')), dtype=np.{self.NPDTYPE})"
    else:
      return f"Decimal({args[0]})"

  ##########################################################################
  # C# methods
  ##########################################################################

  def CSharp_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      commas = ","*(len(self.Dimensinality)-1)  
      return f"decimal[{commas}]" #multidimensional array
    else:
      return "decimal"
  
  def CSharp_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["using System;"] # Consider: System.Numerics.Vectors
    else:
      return []
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"new decimal[{','.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
          return f"{self.DefaultValue}m" #f"(decimal) {self.DefaultValue}M"
      return "0.0m" #"(decimal) 0m"
    
  ##########################################################################
  # Java methods
  ##########################################################################

  def Java_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      brackets = "[]"*(len(self.Dimensinality)) 
      return f"BigDecimal{brackets}" #multidimensional array
    else:
      return "BigDecimal"
  
  def Java_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return ["import java.math.BigDecimal;"]
    else:
      return ["import java.math.BigDecimal;"]
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"new BigDecimal[{']['.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
          return f"BigDecimal.valueOf({self.DefaultValue})" 
      return "BigDecimal.valueOf(0.0)" 