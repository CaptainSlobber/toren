from .TorenObject import TorenObject
import collections
import json

class Module(TorenObject):
  
  def __init__(self):
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentProject = None


  def initializeModule(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentProject = None
    return self


  def setParentProject(self, parentProject):
    self.ParentProject = parentProject



  def todict(self):
    _module = {}
    _module["Name"] = self.Name
    _module["Description"] = self.Description
    _module["ID"]  = self.ID
    return _module

  def tojson(self):
    
    _module_json = json.dumps(self.todict())
    return _module_json
  

  def fromjson(self, jsonString):
    _module = json.loads(jsonString)
    self.fromdict(_module)
    return self

  def fromdict(self, module):
    self.Name= str(module["Name"])
    self.Description = str(module["Description"]) 
    self.ID = str(module["ID"])
    return self