from ..TorenObject import TorenObject
import collections
import json

class Language(TorenObject):
  


  class PropertName():
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"

  class PropertID():
    NAME = "d22beb80-c25f-4404-8cde-87f281b4effc"
    DESCRIPTION = "01e05ec4-2690-4b21-8083-3cbb6acad7bc"
    ID = "dd879086-f7d0-493c-ad69-7d95cfde4081"

  def __init__(self):
    self.Name = "AbstractLanguage"
    self.Description = "Abstract Language"
    self.ID = "e9307c07-c397-4fc0-a472-0c88d8b65cc2"


  def from_dict(self, project):
    self.Name= str(project[self.PropertName.NAME])
    self.Description = str(project[self.PropertName.DESCRIPTION]) 
    self.ID = str(project[self.PropertName.ID])
    return self

  def to_dict(self):
    _langiage = {}
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
