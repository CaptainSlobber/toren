import collections
import json
from .TorenObject import TorenObject
from .Module import Module
from .ModuleCollection import ModuleCollection
from .languages import *
from .datastores import *
from typing import List

class Project(TorenObject):


  class PropertName():
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    VERSION = "Version"
    MODULES = "Modules"
    LANGUAGES = "Languages"
    DATASTORES = "Datastores"
    TYPE = "Type"

  class PropertID():
    NAME = "58795c87-1889-4d2c-8e32-6ae2c8da711b"
    DESCRIPTION = "2ff3a914-ce58-4c59-b444-853521a63e51"
    ID = "5bb456ac-0ba6-4581-9990-f31272c71a4b"
    VERSION = "01d01da2-4492-4d0b-97c0-53b1af0c7b57"
    MODULES = "bf183016-6d32-4950-87a0-1e246a2ffe99" 
    LANGUAGES = "ab43f94f-c692-4318-b8c6-548ab511c6ff"
    DATASTORES = "d4f82402-26dd-484c-b6b0-e50ae4aff2b7"
    TYPE = "06402adf-7222-436a-a542-7791eb9d418a"

  def __init__(self):
    self.Type = "toren.Project"
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.Version = ""
    self.Modules = []
    self.Languages = LanguageCollection()
    self.Datastores = DatabaseCollection()


  def initialize(self, name: str, 
                 description: str, 
                 id: str, 
                 version: str, 
                 modules: list[Module]=None,
                 languages: list[Language] = None,
                 datastores: list[Database] = None):
    self.Type = "toren.Project"
    self.Name = name
    self.Description = description
    self.ID = id
    self.Version = version
    self.Modules = ModuleCollection().initialize(modules, self)
    self.Languages = LanguageCollection().initialize(languages, self)
    self.Datastores = DatabaseCollection().initialize(datastores, self)
    return self

  def to_dict(self):
    _project = {}
    _project[self.PropertName.TYPE] = self.Type
    _project[self.PropertName.NAME] = self.Name
    _project[self.PropertName.DESCRIPTION] = self.Description
    _project[self.PropertName.ID] = self.ID
    _project[self.PropertName.VERSION] = self.Version
    _project[self.PropertName.MODULES] = self.Modules.to_list_of_dict()
    _project[self.PropertName.LANGUAGES] = self.Languages.to_list_of_dict()
    _project[self.PropertName.DATASTORES] = self.Datastores.to_list_of_dict()

    return _project

  def to_json(self):
    _project_json = json.dumps(self.to_dict())
    return _project_json

  def from_json(self, jsonString):
    _project = json.loads(jsonString)
    self.from_dict(_project)
    return self

  def from_dict(self, project):
    #self.ype = str(project[self.PropertName.TYPE])
    self.Name= str(project[self.PropertName.NAME])
    self.Description = str(project[self.PropertName.DESCRIPTION]) 
    self.ID = str(project[self.PropertName.ID])
    self.Version = str(project[self.PropertName.VERSION])
    self.Modules = ModuleCollection().initialize(project[self.PropertName.MODULES], self)
    self.Languages = LanguageCollection().initialize(project[self.PropertName.LANGUAGES], self)
    self.Datastores = DatabaseCollection().initialize(project[self.PropertName.DATASTORES], self)
    return self