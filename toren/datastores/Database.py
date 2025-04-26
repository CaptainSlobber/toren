from ..TorenObject import TorenObject
import collections
import json

class Database(TorenObject):

  class PropertName():
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"

  class PropertID():
    NAME = "df68ea31-f003-4c2e-ac30-134aa067d4ff"
    DESCRIPTION = "d2f9dd1d-4e3e-4300-ad34-5aad7b03915a"
    ID = "7672f241-b819-4613-a18b-f9e8e44d2167"



  def __init__(self):
    self.Name = ""
    self.Description = ""
    self.ID = ""


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Name = name
    self.Description = description
    self.ID = id
    return self



  def from_dict(self, project):
    self.Name= str(project[self.PropertName.NAME])
    self.Description = str(project[self.PropertName.DESCRIPTION]) 
    self.ID = str(project[self.PropertName.ID])
    return self

  def to_dict(self):
    _database = {}
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