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
    OUTPUTDIRECTORY = "OutputDirectory"
    DEFAULTFILEEXTENSION = "DefaultFileExtension"

  class PropertID():
    TYPE = "02dde63e-599f-4195-96e0-9d5b0584145d"
    NAME = "d22beb80-c25f-4404-8cde-87f281b4effc"
    DESCRIPTION = "01e05ec4-2690-4b21-8083-3cbb6acad7bc"
    ID = "dd879086-f7d0-493c-ad69-7d95cfde4081"
    PARENTPROJECT = "dcf42e1a-014a-43a7-b516-0d6f423b7f77"
    OUTPUTDIRECTORY = "e4640152-7b91-4096-93d2-4c260809460b"
    DEFAULTFILEEXTENSION = "6491731a-6b22-4c0c-b2f3-60b7f6f915e1"

  def __init__(self):
    self.initialize()

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    self.DefaultFileExtension = self.getDefaultFileExtension()
    return self

  def getDefaultFileExtension(self):
    return "lang"
  

  def getName(self):
    return "AbstractLanguage"
  
  def getDescription(self):
    return "Abstract Language"

  def getType(self):
    return "toren.languages.Language"
  
  def getID(self):
    return "e9307c07-c397-4fc0-a472-0c88d8b65cc2"

  def setParentProject(self, parentproject):
    self.ParentProject = parentproject

  def from_dict(self, language):
    #self.Type = str(language[self.PropertName.TYPE])
    self.Name= str(language[self.PropertName.NAME])
    self.Description = str(language[self.PropertName.DESCRIPTION]) 
    self.ID = str(language[self.PropertName.ID])
    self.OutputDirectory = str(language[self.PropertName.OUTPUTDIRECTORY])
    self.DefaultFileExtension = str(language[self.PropertName.DEFAULTFILEEXTENSION])
    return self

  def to_dict(self):
    _language = {}
    _language[self.PropertName.TYPE] = self.Type
    _language[self.PropertName.NAME] = self.Name
    _language[self.PropertName.DESCRIPTION] = self.Description
    _language[self.PropertName.ID] = self.ID
    _language[self.PropertName.OUTPUTDIRECTORY] = self.OutputDirectory
    _language[self.PropertName.DEFAULTFILEEXTENSION] = self.DefaultFileExtension
    return _language
  
  def to_json(self):
    _language_json = json.dumps(self.to_dict())
    return _language_json

  def from_json(self, jsonString):
    _language = json.loads(jsonString)
    self.from_dict(_language)
    return self
