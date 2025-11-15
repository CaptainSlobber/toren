from ..TorenObject import TorenObject
from ..languages.Language import Language
from ..languages.LanguageCSharp import LanguageCSharp
from ..languages.LanguageGo import LanguageGo
from ..languages.LanguagePython import LanguagePython
from ..languages.LanguageJavaScript import LanguageJavaScript
from ..languages.LanguageJava import LanguageJava
import collections
import json

class Database(TorenObject):

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTPROJECT = "ParentProject"
    INSTANCENAME = "InstanceName"
    INSTANCEDESCRIPTION = "InstanceDescription"
    INSTANCEID = "InstanceID"

  class PropertID():
    TYPE = "03f73e15-c4d7-4bbf-baa8-25e18e1d1146"
    NAME = "df68ea31-f003-4c2e-ac30-134aa067d4ff"
    DESCRIPTION = "d2f9dd1d-4e3e-4300-ad34-5aad7b03915a"
    ID = "7672f241-b819-4613-a18b-f9e8e44d2167"
    PARENTPROJECT = "cee5a52a-b755-4446-a826-633f0d697be7"
    INSTANCENAME = "28029e15-086d-4fde-9cb5-f8896c6fc69e"
    INSTANCEDESCRIPTION = "15d55be7-02b1-4b14-b88f-c28680a3c1bb"
    INSTANCEID = "e41a26bf-5638-47f3-bc0d-c35f4bdc0101"

  def __init__(self):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.InstanceName = ""
    self.InstanceDescription = ""
    self.InstanceID = ""
    self.ParentProject = None


  def getName(self):
    return "Database"
  
  def getDescription(self):
    return "Database"

  def getType(self):
    return "toren.datastores.Database"
  
  def getID(self):
    return "1a0d0741-65e5-4937-8682-34255fcde015"

  def initialize(self, instanceName: str, 
                 instanceDescription: str, 
                 instanceID: str):
    

    self.Type = self.getType()
    self.InstanceName = instanceName
    self.InstanceDescription = instanceDescription
    self.InstanceID = instanceID
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.ParentProject = None
    return self
  
  def setParentProject(self, parentproject):
    self.ParentProject = parentproject



  def from_dict(self, database):
    #self.Type = str(database[self.PropertName.TYPE])
    self.Name = str(database[self.PropertName.NAME])
    self.Description = str(database[self.PropertName.DESCRIPTION]) 
    self.ID = str(database[self.PropertName.ID])
    self.InstanceName = str(database[self.PropertName.INSTANCENAME])
    self.InstanceDescription = str(database[self.PropertName.INSTANCEDESCRIPTION])
    self.InstanceID = str(database[self.PropertName.INSTANCEID]) 
    return self

  def to_dict(self):
    _database = {}
    _database[self.PropertName.TYPE] = self.Type
    _database[self.PropertName.NAME] = self.Name
    _database[self.PropertName.DESCRIPTION] = self.Description
    _database[self.PropertName.ID] = self.ID
    _database[self.PropertName.INSTANCEID] = self.InstanceName
    _database[self.PropertName.INSTANCENAME] = self.InstanceID
    _database[self.PropertName.INSTANCEDESCRIPTION] = self.InstanceDescription

    return _database
  
  def to_json(self):
    _database_json = json.dumps(self.to_dict())
    return _database_json

  def from_json(self, jsonString):
    _database = json.loads(jsonString)
    self.from_dict(_database)
    return self
  
  ##########################################################################
  # DB Specific Query Syntax
  ##########################################################################

  def OB(self):
    return self.OpenBrackets()
  
  def CB(self):
    return self.CloseBrackets()

  def OpenBrackets(self):
    return "["
  
  def CloseBrackets(self):
    return "]"
  
  def IfNotExists(self):
    return " IF NOT EXISTS"
  
  def IfExists(self):
    return " IF EXISTS"
  
  def EndQuery(self):
    return ";"
  
  def HasSchema(self):
    return True
  
  def GetParameter(self, parmeterNo: int):
    return "*"

  ##########################################################################
  # Dependencies
  ##########################################################################

  def Dependencies(self, language: Language):
    _dep = {}
    _dep[LanguagePython().getID()] = self.PythonDependencies
    _dep[LanguageCSharp().getID()] = self.CSharpDependencies
    _dep[LanguageJava().getID()] = self.JavaDependencies
    _dep[LanguageGo().getID()] = self.GoDependencies
    _dep[LanguageJavaScript().getID()] = self.JavaScriptDependencies
    return _dep[language.ID]()
  
  def ConnectionClass(self, language: Language):
    _conn = {}
    _conn[LanguagePython().getID()] = self.PythonConnectionClass
    _conn[LanguageCSharp().getID()] = self.CSharpConnectionClass
    _conn[LanguageJava().getID()] = self.JavaConnectionClass
    _conn[LanguageGo().getID()] = self.GoConnectionClass
    _conn[LanguageJavaScript().getID()] = self.JavaScriptConnectionClass
    return _conn[language.ID]()

  def CSharpDependencies(self) -> list:
    raise NotImplementedError()
  
  def PythonDependencies(self) -> list:
    raise NotImplementedError()
  
  def JavaDependencies(self) -> list:
    raise NotImplementedError()
  
  def GoDependencies(self) -> list:
    raise NotImplementedError()
  
  def JavaScriptDependencies(self) -> list:
    raise NotImplementedError()
  
  def CSharpConnectionClass(self):
    raise NotImplementedError()
  
  def PythonConnectionClass(self):
    raise NotImplementedError()
  
  def JavaConnectionClass(self):
    raise NotImplementedError()  
  
  def GoConnectionClass(self):
    raise NotImplementedError()   
  
  def JavaScriptConnectionClass(self):
    raise NotImplementedError()