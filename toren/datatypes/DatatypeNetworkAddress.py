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
  
  def Python(self, *args) -> str:
    return "IPv4Address" # TODO: Change to IPv6Address when the time comes
  
  def Python_Dependencies(self) -> list:
    return ["import ipaddress", "from ipaddress import IPv4Address"]
  
  def Python_DefaultValue(self, *args) -> str:
    default_value = "ipaddress.ip_address('0.0.0.0')"
    if self.DefaultValue:
      if len(self.DefaultValue) > 0:
        default_value = f"ipaddress.ip_address('{self.DefaultValue}')"
    return default_value
  