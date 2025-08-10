from ..TorenObject import TorenObject
import collections
import json

class Database(TorenObject):

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTPROJECT = "ParentProject"

  class PropertID():
    TYPE = "03f73e15-c4d7-4bbf-baa8-25e18e1d1146"
    NAME = "df68ea31-f003-4c2e-ac30-134aa067d4ff"
    DESCRIPTION = "d2f9dd1d-4e3e-4300-ad34-5aad7b03915a"
    ID = "7672f241-b819-4613-a18b-f9e8e44d2167"
    PARENTPROJECT = "cee5a52a-b755-4446-a826-633f0d697be7"



  def __init__(self):
    self.Type = "toren.datastores.Database"
    self.Name = "Database"
    self.Description = "Database"
    self.ID = "1a0d0741-65e5-4937-8682-34255fcde015"
    self.ParentProject = None


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.Database"
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentProject = None
    return self
  
  def setParentProject(self, parentproject):
    self.ParentProject = parentproject



  def from_dict(self, database):
    #self.Type = str(database[self.PropertName.TYPE])
    self.Name = str(database[self.PropertName.NAME])
    self.Description = str(database[self.PropertName.DESCRIPTION]) 
    self.ID = str(database[self.PropertName.ID])
    return self

  def to_dict(self):
    _database = {}
    _database[self.PropertName.TYPE] = self.Type
    _database[self.PropertName.NAME] = self.Name
    _database[self.PropertName.DESCRIPTION] = self.Description
    _database[self.PropertName.ID] = self.ID
    return _database
  
  def to_json(self):
    _database_json = json.dumps(self.to_dict())
    return _database_json

  def from_json(self, jsonString):
    _database = json.loads(jsonString)
    self.from_dict(_database)
    return self
  

  def CSharpDependencies(self):
    return [""]
  
  def PythonDependencies(self):
    return [""]
  
  def JavaDependencies(self):
    return [""]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]