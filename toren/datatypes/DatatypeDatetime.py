from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

from datetime import datetime

class DatatypeDatetime(Datatype):

  class PropertName(Datatype.PropertName):
    pass

  class PropertID(Datatype.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeDatetime"
  
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
  
  def unixEpochStart(self):
    # Default to Unix epoch start
    return datetime(1970, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
  
  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################

  def SQLite_Type(self, *args) -> str:
    return "BIGINT"  # SQLite uses TEXT for string/character data

  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"CAST(strftime('%s', '{self.DefaultValue[0]}') AS INT)"
    return "0"

  def PostgreSQL_Type(self, *args) -> str:
    return "TIMESTAMPT"  # TIMESTAMPZ ? 

  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"TO_TIMESTAMP('{self.DefaultValue[0]}', 'YYYY-MM-DD hh24:mi:ss')"
    return f"TO_TIMESTAMP('{self.unixEpochStart()}', 'YYYY-MM-DD hh24:mi:ss')"

  def Oracle_Type(self, *args) -> str:
    return "TIMESTAMP"

  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"TO_TIMESTAMP('{self.DefaultValue[0]}', 'YYYY-MM-DD 24HH:MI:SS')"
    return f"TO_TIMESTAMP('{self.unixEpochStart()}', 'YYYY-MM-DD 24HH:MI:SS')" # SELECT CURRENT_TIMESTAMP FROM DUAL

  def MicrosoftSQL_Type(self, *args) -> str:
    return "DATETIME2"

  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      # 120: yyyy-mm-dd hh:mi:ss (ODBC canonical)
      # 121: yyyy-mm-dd hh:mi:ss.mmm (ODBC canonical with milliseconds)
      return f"CONVERT(DATETIME2, '{self.DefaultValue[0]}', 120)"
    return f"CONVERT(DATETIME2, '{self.unixEpochStart()}', 120)" # "GETDATE()"

  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "datetime" 
  
  def Python_Dependencies(self) -> list:
    return ["from datetime import datetime"]
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"datetime.fromisoformat('{self.DefaultValue}')"
    return "datetime(1970, 1, 1, 0, 0, 0)" 

  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################
  
  def CSharp_Type(self, *args) -> str:
    return "Datetime"
  
  def CSharp_Dependencies(self) -> list:
    return ["using System.Globalization;"]
  
  def CSharp_DefaultValue(self, *args) -> str:
    #default_value = "DateTime.Now"
    #default_value = "DateTime.Parse(\"1970-01-01 00:00:00\", null, DateTimeStyles.RoundtripKind)"
    default_value = 'DateTime.ParseExact("1970-01-01 00:00:00", "yyyy-MM-dd HH:mm:ss", System.Globalization.CultureInfo.InvariantCulture)'
    if self.hasDefaultValue():
        #default_value = f'DateTime.Parse("{self.DefaultValue}", null, DateTimeStyles.RoundtripKind)'
        default_value = f'DateTime.ParseExact("{self.DefaultValue}", "yyyy-MM-dd HH:mm:ss", System.Globalization.CultureInfo.InvariantCulture)'
    return default_value

    