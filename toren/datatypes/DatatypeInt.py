from .DatatypeNumeric import DatatypeNumeric
import collections

class DatatypeInt(DatatypeNumeric):
  
  def __init__(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id