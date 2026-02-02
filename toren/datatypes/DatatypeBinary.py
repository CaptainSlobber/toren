from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeBinary(Datatype):

  class PropertName(Datatype.PropertName):
    SIZELIMITKB = "SizeLimitKB"

  class PropertID(Datatype.PropertID):
    SIZELIMITKB = "80e88ec5-37ae-4ff0-81ac-2ada6a0fb2dc"
  
  def getType(self):
    return "toren.datatypes.DatatypeBinary"
  
  def __init__(self):
    super().__init__()
    self.Type = self.getType()


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 foreignKey: ForeignKey=None,
                 sizeLimitkb: int = 1024):
    
    super().initialize(name = name, 
                 description = description, 
                 id = id,
                 isprimarykey = isprimarykey,
                 isunique=isunique,
                 defaultvalue=defaultvalue,
                 foreignKey=foreignKey)
    self.Type = self.getType()
    self.SizeLimitkb = sizeLimitkb
    return self
  
  def from_dict(self, datatype):
    super().from_dict(datatype)
    self.SizeLimitkb = str(datatype[self.PropertName.SIZELIMITKB])
    self.Type = self.getType()
    return self

  def to_dict(self):
    _datatype = super().to_dict()
    _datatype[self.PropertName.SIZELIMITKB] = self.SizeLimitkb
    return _datatype
  

  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################

  def SQLite_Type(self, *args) -> str:
    return "BLOB"
  
  def SQLite_DefaultValue(self, *args) -> str:
    return self.defaultBlob()
  
  def PostgreSQL_Type(self, *args) -> str:
    return "BYTEA"
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    return self.defaultBlob()
    
  def Oracle_Type(self, *args) -> str:
     return "BLOB"
  
  def Oracle_DefaultValue(self, *args) -> str:
    return self.defaultBlob()
    
  def MicrosoftSQL_Type(self, *args) -> str:
    return "VARBINARY(MAX)"
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    return self.defaultBlob()
  
  ##########################################################################
  # Python methods
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "bytearray"
  
  def Python_Dependencies(self) -> list:
    return []
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"bytearray({self.DefaultValue})"
    return "bytearray()"
  
  def Python_to_Oracle(self, *args) -> str:
    return f"{args[0]}"

  def Python_to_MicrosoftSQL(self, *args) -> str:
    return f"{args[0]}"
  
  def Python_to_PostgreSQL(self, *args) -> str:
    return f"{args[0]}"
  
  def Python_to_SQLite(self, *args) -> str:
    return f"{args[0]}"

  def Python_from_Oracle(self, *args) -> str:
    return f"{args[0]}"
  
  def Python_from_MicrosoftSQL(self, *args) -> str:
    return f"{args[0]}"
  
  def Python_from_PostgreSQL(self, *args) -> str:
    return f"{args[0]}"
  
  def Python_from_SQLite(self, *args) -> str:
    return f"{args[0]}"
  
  ##########################################################################
  # C# methods
  ##########################################################################
  
  def CSharp_Type(self, *args) -> str:
    # TODO: Implement length
    return "byte[]"
  
  def CSharp_Dependencies(self) -> list:
    return []
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"new byte[] {{{self.DefaultValue}}}"
    return "new byte[] {}"
  

  ##########################################################################
  # Java methods
  ##########################################################################
  
  def Java_Type(self, *args) -> str:
    # TODO: Implement length
    return "byte[]"
  
  def Java_Dependencies(self) -> list:
    return []
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
      return f"new byte[] {{{self.DefaultValue}}}"
    return "new byte[] {}"
  
  ##########################################################################
  # Java methods for converting to and from various database types
  ##########################################################################

  def _Java_to_(self, *args)-> str:
    argt = args[0][0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'statement.setBytes({indx}, {objname}.get{propertyname}());'
    return setval

  def Java_to_Oracle(self, *args) -> str:
    return self._Java_to_(args)
  
  def Java_to_MicrosoftSQL(self, *args) -> str:
    return self._Java_to_(args)
  
  def Java_to_PostgreSQL(self, *args) -> str:
    return self._Java_to_(args)
  
  def Java_to_SQLite(self, *args) -> str:
    return self._Java_to_(args)