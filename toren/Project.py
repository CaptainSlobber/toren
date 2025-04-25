import collections
import json
from .TorenObject import TorenObject
from .Module import Module

class Project(TorenObject):


  class PropertName():
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    VERSION = "Version"
    MODULES = "Modules"

  class PropertID():
    NAME = "58795c87-1889-4d2c-8e32-6ae2c8da711b"
    DESCRIPTION = "2ff3a914-ce58-4c59-b444-853521a63e51"
    ID = "5bb456ac-0ba6-4581-9990-f31272c71a4b"
    VERSION = "01d01da2-4492-4d0b-97c0-53b1af0c7b57"
    MODULES = "bf183016-6d32-4950-87a0-1e246a2ffe99" 

  def __init__(self):
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.Version = ""
    self.Modules = []


  def initialize(self, name: str, description: str, id: str, version: str, modules: list=None):
    self.Name = name
    self.Description = description
    self.ID = id
    self.Version = version
    self.Modules = self.setModules(modules)
    return self

  def setModulesFromList(self, modules):

    _modules =collections.OrderedDict()
    if not modules is None:
      for module in modules:
        if isinstance(module, dict): module = Module().from_dict(module)
        module.setParentProject(self)
        _modules[module.ID] = module
    return _modules

  def setModules(self, modules):
    return self.setModulesFromList(modules)

  def setModulesFromDict(self, modules):

    _modules =collections.OrderedDict()
    for key, module in modules.items():
      if isinstance(module, dict): module = Module().from_dict(module)
      module.setParentProject(self)
      _modules[key] = module
    return _modules

  def to_dict(self):
    _project = {}
    _project[self.PropertName.NAME] = self.Name
    _project[self.PropertName.DESCRIPTION] = self.Description
    _project[self.PropertName.ID] = self.ID
    _project[self.PropertName.VERSION] = self.Version
    _project[self.PropertName.MODULES] = [m.to_dict() for m in list(self.Modules.values())]
    return _project

  def to_json(self):
    
    _project_json = json.dumps(self.to_dict())
    return _project_json

  def from_json(self, jsonString):
    _project = json.loads(jsonString)
    self.from_dict(_project)
    return self

  def from_dict(self, project):
    self.Name= str(project[self.PropertName.NAME])
    self.Description = str(project[self.PropertName.DESCRIPTION]) 
    self.ID = str(project[self.PropertName.ID])
    self.Version = str(project[self.PropertName.VERSION])
    self.Modules = self.setModules(project[self.PropertName.MODULES])
    return self