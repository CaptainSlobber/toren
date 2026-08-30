from .Datatype import Datatype
from .ForeignKey import ForeignKey
import collections
import uuid

class DatatypeUUID(Datatype):

  class PropertName(Datatype.PropertName):
    pass

  class PropertID(Datatype.PropertID):
    pass
  
  def getType(self):
    return "toren.datatypes.DatatypeUUID"
  
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
  

  def isUUID(uuidstr, version=4):
    try:
        uuid_obj = uuid.UUID(uuidstr, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuidstr
  
  ##########################################################################
  # Database Property Types and Default Values
  ##########################################################################
   
  def SQLite_Type(self, *args) -> str:
    return f"NVARCHAR(36)" 
  
  def SQLite_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return self._DefaultValueSingleQuote()
    return self._SingleQuote("")

  def PostgreSQL_Type(self, *args) -> str:
    return f"UUID"
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return f"CAST({self._SingleQuote(self.DefaultValue)} AS uuid)" # f"{self._SingleQuote(self.DefaultValue)}::uuid" 
    return "uuid_generate_v4()" # gen_random_uuid()
    
  def Oracle_Type(self, *args) -> str:
     return f"NVARCHAR2(36)" # RAW(16) ?
  
  def Oracle_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return self._DefaultValueSingleQuote()
    return self._SingleQuote("")
  
  def MicrosoftSQL_Type(self, *args) -> str:
    return f"UNIQUEIDENTIFIER"
  
  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return f"CONVERT(UNIQUEIDENTIFIER, {self._DefaultValueSingleQuote()})" 
    return "NEWID()" # NEWSEQUENTIALID()
  
  ##########################################################################
  # Python methods
  ##########################################################################

  def Python_Type(self, *args) -> str:
    return "uuid.UUID"
  
  def Python_Dependencies(self) -> list:
    return ['import uuid']
  
  def Python_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return f"uuid.UUID({self._DefaultValueSingleQuote()})"
    return "uuid.uuid4()"
  
  def Python_to_Oracle(self, *args) -> str:
    return f"str({args[0]})"

  def Python_to_MicrosoftSQL(self, *args) -> str:
    return f"str({args[0]})"
  
  def Python_to_PostgreSQL(self, *args) -> str:
    return f"str({args[0]})"
  
  def Python_to_SQLite(self, *args) -> str:
    return f"str({args[0]})"

  def Python_from_Oracle(self, *args) -> str:
    return f"uuid.UUID({args[0]})"
  
  def Python_from_MicrosoftSQL(self, *args) -> str:
    return f"uuid.UUID({args[0]})"
  
  def Python_from_PostgreSQL(self, *args) -> str:
    return f"uuid.UUID({args[0]})"
  
  def Python_from_SQLite(self, *args) -> str:
    return f"uuid.UUID({args[0]})"
  
  ##########################################################################
  # C# methods
  ##########################################################################

  def CSharp_Type(self, *args) -> str:
    return "System.Guid"
  
  def CSharp_Dependencies(self) -> list:
    return ["using System;"] 
  
  def CSharp_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return f' Guid.Parse({self._DefaultValueDoubleQuote})'
    return 'System.Guid.NewGuid()'

  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################

  def _CSharp_to_(self, *args)-> str:
    argt = args[0][0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'{objname}.{propertyname}'
    return setval

  def CSharp_to_Oracle(self, *args) -> str:
    argt = args[0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'{objname}.{propertyname}'
    settype = f'OracleDbType.NVarchar2'
    return f'{{param_value_key, {setval}}}, {{param_dbtype_key, {settype}}}'
  
  def CSharp_to_MicrosoftSQL(self, *args) -> str:
    argt = args[0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'{objname}.{propertyname}'
    settype = f'SqlDbType.UniqueIdentifier'
    return f'{{param_value_key, {setval}}}, {{param_dbtype_key, {settype}}}'
  
  def CSharp_to_PostgreSQL(self, *args) -> str:
    argt = args[0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'{objname}.{propertyname}'
    settype = f'NpgsqlDbType.Uuid'
    return f'{{param_value_key, {setval}}}, {{param_dbtype_key, {settype}}}'
  
  def CSharp_to_SQLite(self, *args) -> str:
    argt = args[0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'{objname}.{propertyname}'
    settype = f'"{self.SQLite_Type()}"'
    return f'{{param_value_key, {setval}}}, {{param_dbtype_key, {settype}}}' 

  ##########################################################################
  # C# methods for converting from various database types
  ##########################################################################

  def CSharp_from_Oracle(self, *args) -> str:
    return self.CSharp_from_(args[0])
  
  def CSharp_from_MicrosoftSQL(self, *args) -> str:
    return self.CSharp_from_(args[0])
  
  def CSharp_from_PostgreSQL(self, *args) -> str:
    return self.CSharp_from_(args[0])
  
  def CSharp_from_SQLite(self, *args) -> str:
    return f'Guid.Parse((string){args[0]})'

  def CSharp_from_(self, *args) -> str:
    argt = args
    return f"(System.Guid){argt[0]}"    

  ##########################################################################
  # Java methods
  ##########################################################################

  def Java_Type(self, *args) -> str:
    return "UUID"
  
  def Java_Dependencies(self) -> list:
    return ["import java.util.UUID;"] 
  
  def Java_DefaultValue(self, *args) -> str:
    if self.hasDefaultValue() and self.isUUID(self.DefaultValue):
        return f'UUID.fromString({self._DefaultValueDoubleQuote})'
    return 'UUID.randomUUID()'
  
  ##########################################################################
  # Java methods for converting to and from various database types
  ##########################################################################

  def _Java_to_(self, *args)-> str:
    argt = args[0][0]
    indx = str(int(argt[0]))
    objname = str(argt[1])
    propertyname = str(argt[2])
    setval = f'statement.setObject({indx}, {objname}.get{propertyname}());'
    return setval

  def Java_to_Oracle(self, *args) -> str:
    return self._Java_to_(args)
  
  def Java_to_MicrosoftSQL(self, *args) -> str:
    return self._Java_to_(args)
  
  def Java_to_PostgreSQL(self, *args) -> str:
    return self._Java_to_(args)
  
  def Java_to_SQLite(self, *args) -> str:
    return self._Java_to_(args)