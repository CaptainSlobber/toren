from .TorenObject import TorenObject
import collections

class Module(TorenObject):
  
  def __init__(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentProject = None

  def setParentProject(self, parentProject):
    self.ParentProject = parentProject
