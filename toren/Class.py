from .TorenObject import TorenObject
import collections

class Class(TorenObject):
  
  def __init__(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentModule = None

  def setParentModule(self, parentModule):
    self.ParentModule = parentModule

    
