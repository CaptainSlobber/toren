from .Datatype import Datatype
from .ForeignKey import ForeignKey
from .DatatypeNumeric import DatatypeNumeric
import math
import collections

class DatatypeInt(DatatypeNumeric):

  class PropertName(DatatypeNumeric.PropertName):
    pass

  class PropertID(DatatypeNumeric.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeInt"
  
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
      return "INT" # https://www.sqlite.org/datatype3.html
  
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
      return f"INT"
  
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
      return f"INT" # INTEGER
  
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
      return f"INT"
  
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
    if len(self.Dimensinality) > 0:
      return f"npt.NDArray[np.int32]" #np.array/np.ndarray
    else:
      return "int"
  
  def Python_Dependencies(self) -> list:
    if len(self.Dimensinality) > 0:
      return ["import numpy as np", "import numpy.typing as npt", "import json"]
    else:
      return []
  
  def Python_DefaultValue(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      return f"np.zeros({str(self.Dimensinality)}, dtype=np.int32)"
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
    
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
      return f"np.array(json.loads({args[0]}.decode('utf-8')), dtype=np.int32)"
    else:
      return f"int({args[0]})"
  
  def Python_from_MicrosoftSQL(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads({args[0]}.decode('utf-8')), dtype=np.int32)"
    else:
      return f"int({args[0]})"
  
  def Python_from_PostgreSQL(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads({args[0]}.decode('utf-8')), dtype=np.int32)"
    else:
      return f"int({args[0]})"
  
  def Python_from_SQLite(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"np.array(json.loads({args[0]}.decode('utf-8')), dtype=np.int32)"
    else:
      return f"int({args[0]})"
    
  ##########################################################################
  # C# methods
  ##########################################################################
    
  def CSharp_Type(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      commas = ","*(len(self.Dimensinality)-1)  
      return f"int[{commas}]" #multidimensional array
    else:
      return "int"
  
  def CSharp_Dependencies(self) -> list:
    if len(self.Dimensinality) > 0:
      return ["using System;"] # Consider: System.Numerics.Vectors
    else:
      return []
  
  def CSharp_DefaultValue(self, *args) -> str:
    if len(self.Dimensinality) > 0:
      return f"new int[{','.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
        return f"{str(int(self.DefaultValue))}"
      return "0"
    
  ##########################################################################
  # Java methods
  ##########################################################################
  
  def Java_Type(self, *args) -> str:
    if self.hasHigherDimensionality():
      brackets = "[]"*(len(self.Dimensinality)) 
      return f"int{brackets}" #multidimensional array
    else:
      return "int"
  
  def Java_Dependencies(self) -> list:
    if self.hasHigherDimensionality():
      return []
    else:
      return []
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasHigherDimensionality():
      return f"new int[{']['.join(list(map(str, self.Dimensinality)))}]"
    else:
      if self.hasDefaultValue():
          return f"{self.DefaultValue}" 
      return "0" 