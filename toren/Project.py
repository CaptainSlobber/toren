import collections
import json
from .TorenObject import TorenObject
from .Module import Module

class Project(TorenObject):
  def __init__(self):
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.Modules = []


  def initializeProject(self, name: str, description: str, id: str, modules: list=None):
    self.Name = name
    self.Description = description
    self.ID = id
    self.Modules = self.setModules(modules)
    return self

  def setModulesFromList(self, modules):

    _modules =collections.OrderedDict()
    if not modules is None:
      for module in modules:
        if isinstance(module, dict): module = Module().fromdict(module)
        module.setParentProject(self)
        _modules[module.ID] = module
    return _modules

  def setModules(self, modules):
    return self.setModulesFromList(modules)

  def setModulesFromDict(self, modules):

    _modules =collections.OrderedDict()
    for key, module in modules.items():
      if isinstance(module, dict): module = Module().fromdict(module)
      module.setParentProject(self)
      _modules[key] = module
    return _modules

  def todict(self):
    _project = {}
    _project["Name"] = self.Name
    _project["Description"] = self.Description
    _project["ID"]  = self.ID
    _project["Modules"] = [m.todict() for m in list(self.Modules.values())]
    return _project

  def tojson(self):
    
    _project_json = json.dumps(self.todict())
    return _project_json

  def fromjson(self, jsonString):
    _project = json.loads(jsonString)
    self.fromdict(_project)
    return self

  def fromdict(self, project):
    self.Name= str(project["Name"])
    self.Description = str(project["Description"]) 
    self.ID = str(project["ID"])

    self.Modules = self.setModules(project["Modules"])
    return self