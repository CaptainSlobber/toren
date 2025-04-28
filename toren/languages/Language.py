from ..TorenObject import TorenObject
import collections
import json

class Language(TorenObject):
  

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTPROJECT = "ParentProject"

  class PropertID():
    TYPE = "02dde63e-599f-4195-96e0-9d5b0584145d"
    NAME = "d22beb80-c25f-4404-8cde-87f281b4effc"
    DESCRIPTION = "01e05ec4-2690-4b21-8083-3cbb6acad7bc"
    ID = "dd879086-f7d0-493c-ad69-7d95cfde4081"
    PARENTPROJECT = "dcf42e1a-014a-43a7-b516-0d6f423b7f77"

  def __init__(self):
    self.initialize()

  def initialize(self):
    self.Type = "toren.languages.Language"
    self.Name = "AbstractLanguage"
    self.Description = "Abstract Language"
    self.ID = "e9307c07-c397-4fc0-a472-0c88d8b65cc2"
    self.ParentProject = None

  def setParentProject(self, parentproject):
    self.ParentProject = parentproject

  def from_dict(self, language):
    #self.Type = str(language[self.PropertName.TYPE])
    self.Name= str(language[self.PropertName.NAME])
    self.Description = str(language[self.PropertName.DESCRIPTION]) 
    self.ID = str(language[self.PropertName.ID])
    return self

  def to_dict(self):
    _langiage = {}
    _langiage[self.PropertName.TYPE] = self.Type
    _langiage[self.PropertName.NAME] = self.Name
    _langiage[self.PropertName.DESCRIPTION] = self.Description
    _langiage[self.PropertName.ID] = self.ID
    return _langiage
  
  def to_json(self):
    _langiage_json = json.dumps(self.to_dict())
    return _langiage_json

  def from_json(self, jsonString):
    _langiage = json.loads(jsonString)
    self.from_dict(_langiage)
    return self
