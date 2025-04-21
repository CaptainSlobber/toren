from .Datatype import Datatype
import collections

class DatatypeDatetime(Datatype):
  
  def __init__(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id