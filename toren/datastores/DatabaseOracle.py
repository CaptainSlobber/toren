from .Database import Database
import collections

class DatabaseOracle(Database):
  
  def __init__(self):
    self.Type = "toren.datastores.DatabaseOracle"
    self.Name = ""
    self.Description = ""
    self.ID = ""


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.DatabaseOracle"
    self.Name = name
    self.Description = description
    self.ID = id
    return self