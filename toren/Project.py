from .TorenObject import TorenObject

class Project(TorenObject):
  def __init__(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id