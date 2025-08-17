from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections

class DatatypeNetworkAddress(Datatype):

  class PropertName(Datatype.PropertName):
    pass

  class PropertID(Datatype.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeNetworkAddress"
  
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

  def _Default_Address(self):
    return '127.0.0.1'

  def _Default_Address_Integer(self, address: str) -> int:
    a = ""
    s = address.split('.'  )
    for i in s:
      a = a + f'{i:03}'
    return int(a.join())
  
  def _Default_Address_Str(self, address: str) -> str:
    return str(self._Default_Address_Integer(address))

  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
   
  def SQLite_Type(self, *args) -> str:
    return "BIGINT"
  
  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._Default_Address_Str(self.DefaultValue)
    return self._Default_Address_Str(self._Default_Address())

  def PostgreSQL_Type(self, *args) -> str:
    # Consider: https://www.postgresql.org/docs/current/datatype-net-types.html
    return "BIGINT"
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._Default_Address_Str(self.DefaultValue)
    return self._Default_Address_Str(self._Default_Address())
    
  def Oracle_Type(self, *args) -> str:
     return "BIGINT"
  
  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._Default_Address_Str(self.DefaultValue)
    return self._Default_Address_Str(self._Default_Address())
    
  def MicrosoftSQL_Type(self, *args) -> str:
    return "BIGINT"
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return self._Default_Address_Str(self.DefaultValue)
    return self._Default_Address_Str(self._Default_Address())
  
  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################
  
  def Python_Type(self, *args) -> str:
    return "IPv4Address" # TODO: Change to IPv6Address when the time comes
  
  def Python_Dependencies(self) -> list:
    return ["import ipaddress", "from ipaddress import IPv4Address"]
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return f"ipaddress.ip_address('{self.DefaultValue}')"
    return f"ipaddress.ip_address('{self._Default_Address()}')" 
  
  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################

  def CSharp_Type(self, *args) -> str:
    return "IPAddress"
  
  def CSharp_Dependencies(self) -> list:
    return ["using System;", "using System.Net;"] 
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue():
        return f'IPAddress.Parse("{self.DefaultValue}")'
    return f'IPAddress.Parse("{self._Default_Address()}")'