from ..TorenObject import TorenObject
from .ForeignKey import ForeignKey
from ..languages.Language import Language
from ..languages.LanguageCSharp import LanguageCSharp
from ..languages.LanguagePython import LanguagePython
from ..languages.LanguageJava import LanguageJava
from ..languages.LanguageGo import LanguageGo
from ..languages.LanguageJavaScript import LanguageJavaScript
from ..datastores.Database import Database
from ..datastores.DatabaseSQLite import DatabaseSQLite
from ..datastores.DatabaseMicrosoftSQL import DatabaseMicrosoftSQL
from ..datastores.DatabaseOracle import DatabaseOracle
from ..datastores.DatabasePostgreSQL import DatabasePostgreSQL
from ..languages.LanguageTranslator import LanguageTranslator
from ..languages.LanguageDatastoreConverter import LanguageDatastoreConverter
import collections
import json

class Datatype(TorenObject):

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTMODULE = "ParentModule"
    ISPRIMARYKEY = "IsPrimaryKey"
    ISUNIQUE = "IsUnique"
    DEFAULTVALUE = "DefaultValue"
    FOREIGNKEY = "ForeignKey"
    ALLOWNULLS = "AllowNulls"


  class PropertID():
    TYPE = "3b44d998-ef93-4d3c-b01f-fea888f7ad8d"
    NAME = "4310715d-f631-44f4-b0b8-8e56c90547d9"
    DESCRIPTION = "e75bc526-8ae7-4f23-943a-73bc9448edc4"
    ID = "a066d0fc-392f-44ea-bbd6-da6e71bf7002"
    PARENTMODULE = "ea08aad9-b34b-4990-9b85-572841672f62"
    ISPRIMARYKEY = "ea0ebb8c-57e7-4c36-b834-132dd1329690"
    ISUNIQUE = "01a9e2b8-3a64-4832-bb01-ce05120fb9f8"
    DEFAULTVALUE = "e9009d06-73ed-4e73-a5bb-4836badf4037"
    FOREIGNKEY = "f3553d5e-f65f-4a70-b45f-1db6ccb714b1"
    ALLOWNULLS = "23222ba3-c0e0-4d4b-bdba-5c34ec13016d"

  def getType(self):
    return "toren.datatypes.Datatype"
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentModule = None
    self.IsPrimaryKey = False
    self.IsUnique = False
    self.DefaultValue = ""
    self.ForeignKey = None
    self.AllowNulls = False


  def initialize(self, name: str, 
                 description: str, 
                 id: str,
                 isprimarykey: bool = False,
                 isunique: bool = False,
                 defaultvalue: str = "",
                 foreignKey: ForeignKey=None):
    self.Type = self.getType()
    self.Name = name.strip()
    self.Description = description.strip()
    self.ID = id.strip()
    self.ParentModule = None
    self.IsPrimaryKey = isprimarykey
    self.IsUnique = isunique
    self.DefaultValue = defaultvalue
    self.ForeignKey = foreignKey
    self.AllowNulls = False
    return self
  

  def getFlattenedMatrixCharacterLimit(self):
    # PostgreSQL VARCHAR(n) n = 10,485,760
    # Microsoft SQL Server VARCHAR(n) n 8000 bytes
    # Microsoft SQL Server VARCHAR(MAX) 2^31-1 bytes
    # SQLite SQLITE_MAX_LENGTH = 1 billion bytes (1 GB)
    # Oracle MAX_STRING_SIZE for VARCHAR2 is 4000 bytes or characters
    return 1024
  
  def getFlattenedMatrixParameterCountLimit(self):
    return 1024
  
  def setParentClass(self, parentclass):
    self.ParentClass = parentclass
    return self

  def setForeignKey(self, foreignkeypropertyname, foreignkeyclassproperty, foreignkeyclass=None):
    self.ForeignKey = ForeignKey().initialize(foreignkeypropertyname, foreignkeyclassproperty, foreignkeyclass)
    return self

  def from_dict(self, datatype):
    self.Type = self.getType()
    self.Name= str(datatype[self.PropertName.NAME])
    self.Description = str(datatype[self.PropertName.DESCRIPTION]) 
    self.ID = str(datatype[self.PropertName.ID])
    self.IsPrimaryKey = bool(datatype[self.PropertName.ISPRIMARYKEY])
    self.IsUnique = bool(datatype[self.PropertName.ISUNIQUE])
    self.AllowNulls = bool(datatype[self.PropertName.ALLOWNULLS])
    self.DefaultValue = str(datatype[self.PropertName.DEFAULTVALUE])
    
    if self.PropertName.FOREIGNKEY in datatype: 
      self.ForeignKey = ForeignKey().from_dict(datatype[self.PropertName.FOREIGNKEY])
    return self

  def to_dict(self):
    _datatype = {}
    _datatype[self.PropertName.TYPE] = self.Type
    _datatype[self.PropertName.NAME] = self.Name
    _datatype[self.PropertName.DESCRIPTION] = self.Description
    _datatype[self.PropertName.ID] = self.ID
    _datatype[self.PropertName.ISPRIMARYKEY] = self.IsPrimaryKey
    _datatype[self.PropertName.ISUNIQUE] = self.IsUnique
    _datatype[self.PropertName.ALLOWNULLS] = self.AllowNulls
    _datatype[self.PropertName.DEFAULTVALUE] = self.DefaultValue

    if self.ForeignKey is not None: 
      _datatype[self.PropertName.FOREIGNKEY] = self.ForeignKey.to_dict()
    return _datatype
  
  def to_json(self):
    _datatype_json = json.dumps(self.to_dict())
    return _datatype_json

  def from_json(self, jsonString):
    _datatype = json.loads(jsonString)
    self.from_dict(_datatype)
    return self
  
  ##########################################################################
  # Common Operations
  ##########################################################################

  def defaultBlob(self):
    return "0x00"

  def hasDefaultValue(self):
    if self.DefaultValue is not None:
      if len(self.DefaultValue) > 0:
        return True
    return False
  
  def _Escape_String(self, value: str) -> str:
    if value is None:
      return ""
    if isinstance(value, str):
      return value.replace("'", "''").replace("\"","\"")  # Escape single quotes for SQL
    return ""
    
  def _DefaultValueSingleQuote(self) -> str:
    return  self._SingleQuote(self.DefaultValue)
  
  def _DefaultValueDoubleQuote(self) -> str:
    return  self._DoubleQuote(self.DefaultValue)
  
  def _SingleQuote(self, val: str)-> str:
    return  f"'{self._Escape_String(val)}'"
  
  def _DoubleQuote(self, val: str)-> str:
    return  f"\"{self._Escape_String(val)}\""
  
  ##########################################################################
  # To
  ##########################################################################

  def To(self, language: Language, database: Database, *args) -> str:
    _to = {}
    _to[f"{LanguagePython().getID()}{DatabaseSQLite().getID()}"] = self.Python_to_SQLite
    _to[f"{LanguagePython().getID()}{DatabasePostgreSQL().getID()}"] = self.Python_to_PostgreSQL
    _to[f"{LanguagePython().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.Python_to_MicrosoftSQL
    _to[f"{LanguagePython().getID()}{DatabaseOracle().getID()}"] = self.Python_to_Oracle

    _to[f"{LanguageCSharp().getID()}{DatabaseSQLite().getID()}"] = self.CSharp_to_SQLite
    _to[f"{LanguageCSharp().getID()}{DatabasePostgreSQL().getID()}"] = self.CSharp_to_PostgreSQL
    _to[f"{LanguageCSharp().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.CSharp_to_MicrosoftSQL
    _to[f"{LanguageCSharp().getID()}{DatabaseOracle().getID()}"] = self.CSharp_to_Oracle

    _to[f"{LanguageJava().getID()}{DatabaseSQLite().getID()}"] = self.Java_to_SQLite
    _to[f"{LanguageJava().getID()}{DatabasePostgreSQL().getID()}"] = self.Java_to_PostgreSQL
    _to[f"{LanguageJava().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.Java_to_MicrosoftSQL
    _to[f"{LanguageJava().getID()}{DatabaseOracle().getID()}"] = self.Java_to_Oracle

    _to[f"{LanguageGo().getID()}{DatabaseSQLite().getID()}"] = self.Go_to_SQLite
    _to[f"{LanguageGo().getID()}{DatabasePostgreSQL().getID()}"] = self.Go_to_PostgreSQL
    _to[f"{LanguageGo().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.Go_to_MicrosoftSQL
    _to[f"{LanguageGo().getID()}{DatabaseOracle().getID()}"] = self.Go_to_Oracle

    _to[f"{LanguageJavaScript().getID()}{DatabaseSQLite().getID()}"] = self.JavaScript_to_SQLite
    _to[f"{LanguageJavaScript().getID()}{DatabasePostgreSQL().getID()}"] = self.JavaScript_to_PostgreSQL
    _to[f"{LanguageJavaScript().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.JavaScript_to_MicrosoftSQL
    _to[f"{LanguageJavaScript().getID()}{DatabaseOracle().getID()}"] = self.JavaScript_to_Oracle

    return _to[f"{language.getID()}{database.getID()}"](args[0])


  ##########################################################################
  # From
  ##########################################################################

  def From(self, language: Language, database: Database, *args) -> str:
    _from = {}
    _from[f"{LanguagePython().getID()}{DatabaseSQLite().getID()}"] = self.Python_from_SQLite
    _from[f"{LanguagePython().getID()}{DatabasePostgreSQL().getID()}"] = self.Python_from_PostgreSQL
    _from[f"{LanguagePython().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.Python_from_MicrosoftSQL
    _from[f"{LanguagePython().getID()}{DatabaseOracle().getID()}"] = self.Python_from_Oracle

    _from[f"{LanguageCSharp().getID()}{DatabaseSQLite().getID()}"] = self.CSharp_from_SQLite
    _from[f"{LanguageCSharp().getID()}{DatabasePostgreSQL().getID()}"] = self.CSharp_from_PostgreSQL
    _from[f"{LanguageCSharp().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.CSharp_from_MicrosoftSQL
    _from[f"{LanguageCSharp().getID()}{DatabaseOracle().getID()}"] = self.CSharp_from_Oracle

    _from[f"{LanguageJava().getID()}{DatabaseSQLite().getID()}"] = self.Java_from_SQLite
    _from[f"{LanguageJava().getID()}{DatabasePostgreSQL().getID()}"] = self.Java_from_PostgreSQL
    _from[f"{LanguageJava().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.Java_from_MicrosoftSQL
    _from[f"{LanguageJava().getID()}{DatabaseOracle().getID()}"] = self.Java_from_Oracle

    _from[f"{LanguageGo().getID()}{DatabaseSQLite().getID()}"] = self.Go_from_SQLite
    _from[f"{LanguageGo().getID()}{DatabasePostgreSQL().getID()}"] = self.Go_from_PostgreSQL
    _from[f"{LanguageGo().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.Go_from_MicrosoftSQL
    _from[f"{LanguageGo().getID()}{DatabaseOracle().getID()}"] = self.Go_from_Oracle

    _from[f"{LanguageJavaScript().getID()}{DatabaseSQLite().getID()}"] = self.JavaScript_from_SQLite
    _from[f"{LanguageJavaScript().getID()}{DatabasePostgreSQL().getID()}"] = self.JavaScript_from_PostgreSQL
    _from[f"{LanguageJavaScript().getID()}{DatabaseMicrosoftSQL().getID()}"] = self.JavaScript_from_MicrosoftSQL
    _from[f"{LanguageJavaScript().getID()}{DatabaseOracle().getID()}"] = self.JavaScript_from_Oracle

    return _from[f"{language.ID}{database.ID}"](args[0])
  
  ##########################################################################
  # Dependencies
  ##########################################################################

  def Dependencies(self, language: Language) -> str:
    _dep = {}
    _dep[LanguagePython().getID()] = self.Python_Dependencies
    _dep[LanguageCSharp().getID()] = self.CSharp_Dependencies
    _dep[LanguageJava().getID()] = self.Java_Dependencies
    _dep[LanguageGo().getID()] = self.Go_Dependencies
    _dep[LanguageJavaScript().getID()] = self.JavaScript_Dependencies
    return _dep[language.ID]()
  
  ##########################################################################
  # Language Default fValue
  ##########################################################################

  def LanguageDefaultfValue(self, language: Language) -> str:
    _dv = {}
    _dv[LanguagePython().getID()] = self.Python_DefaultValue
    _dv[LanguageCSharp().getID()] = self.CSharp_DefaultValue
    _dv[LanguageJava().getID()] = self.Java_DefaultValue
    _dv[LanguageGo().getID()] = self.Go_DefaultValue
    _dv[LanguageJavaScript().getID()] = self.JavaScript_DefaultValue
    return _dv[language.ID]()
  
  ##########################################################################
  # Property Type
  ##########################################################################

  def PropertyType(self, language: Language) -> str:
    _pt = {}
    _pt[LanguagePython().getID()] = self.Python_Type
    _pt[LanguageCSharp().getID()] = self.CSharp_Type
    _pt[LanguageJava().getID()] = self.Java_Type
    _pt[LanguageGo().getID()] = self.Go_Type
    _pt[LanguageJavaScript().getID()] = self.JavaScript_Type
    return _pt[language.ID]()
  

  ##########################################################################
  # Database Property Types
  ##########################################################################
  def DatabasePropertyType(self, database: Database) -> str:
    _pt = {}
    _pt[DatabaseMicrosoftSQL().getID()] = self.MicrosoftSQL_Type
    _pt[DatabaseOracle().getID()] = self.Oracle_Type
    _pt[DatabasePostgreSQL().getID()] = self.PostgreSQL_Type
    _pt[DatabaseSQLite().getID()] = self.SQLite_Type
    return _pt[database.ID]()

  def MicrosoftSQL_Type(self, *args) -> str:
    raise NotImplementedError
  
  def Oracle_Type(self, *args) -> str:
    raise NotImplementedError
  
  def PostgreSQL_Type(self, *args) -> str:
    raise NotImplementedError
  
  def SQLite_Type(self, *args) -> str:
    raise NotImplementedError
  
  ##########################################################################
  # Database Default Value
  ##########################################################################
  def DatabaseDefaultValue(self, database: Database) -> str:
    _dv = {}
    _dv[DatabaseMicrosoftSQL.getID()] = self.MicrosoftSQL_DefaultValue
    _dv[DatabaseOracle.getID()] = self.Oracle_DefaultValue
    _dv[DatabasePostgreSQL.getID()] = self.PostgreSQL_DefaultValue
    _dv[DatabaseSQLite.getID()] = self.SQLite_DefaultValue
    return _dv[database.ID]()

  def MicrosoftSQL_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  def Oracle_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  def PostgreSQL_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  def SQLite_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  ##########################################################################
  # Python methods for converting to and from various database types
  ##########################################################################
  def Python_Helper_Functions(self, s):
    return s
  
  def Python_Type(self, *args) -> str:
    raise NotImplementedError
  
  def Python_Dependencies(self) -> list:
    return NotImplementedError
  
  def Python_DefaultValue(self, *args) -> str:
    return NotImplementedError
  
  def Python_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Python_to_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def Python_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Python_from_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Python_from_SQLite(self, *args) -> str:
    raise NotImplementedError

  ##########################################################################
  # Java methods for converting to and from various database types
  ##########################################################################
  def Java_Helper_Functions(self, s):
    return s
  
  def Java_Type(self, *args) -> str:
    raise NotImplementedError
  
  def Java_Dependencies(self, *args) -> str:
    raise NotImplementedError
  
  def Java_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def Java_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Java_from_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Java_from_SQLite(self, *args) -> str:
    raise NotImplementedError
  
  ##########################################################################
  # C# methods for converting to and from various database types
  ##########################################################################
  def CSharp_Helper_Functions(self, s):
    return s
  
  def CSharp_Type(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_Dependencies(self) -> list:
    return NotImplementedError

  def CSharp_DefaultValue(self, *args) -> str:
    return NotImplementedError
  
  def CSharp_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def CSharp_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_from_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def CSharp_from_SQLite(self, *args) -> str:
    raise NotImplementedError

  #########################################################################
  # Go methods for converting to and from various database types
  ##########################################################################
  def Go_Helper_Functions(self, s):
    return s
  
  def Go_Type(self, *args) -> str:
    raise NotImplementedError
  
  def Go_Dependencies(self, *args) -> str:
    raise NotImplementedError
  
  def Go_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def Go_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def Go_from_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def Go_from_SQLite(self, *args) -> str:
    raise NotImplementedError

  #########################################################################
  # JavaScript methods for converting to and from various database types
  ##########################################################################
  def JavaScript_Helper_Functions(self, s):
    return s
  
  def JavaScript_Type(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_Dependencies(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_DefaultValue(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_to_SQLite(self, *args) -> str:
    raise NotImplementedError

  def JavaScript_from_Oracle(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_from_MicrosoftSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_from_PostgreSQL(self, *args) -> str:
    raise NotImplementedError
  
  def JavaScript_from_SQLite(self, *args) -> str:
    raise NotImplementedError
  

