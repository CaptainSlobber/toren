from .Database import Database
import collections

class DatabaseSQLite(Database):
  
  def __init__(self):
    self.Type = "toren.datastores.DatabaseSQLite"
    self.Name = ""
    self.Description = ""
    self.ID = ""


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.DatabaseSQLite"
    self.Name = name
    self.Description = description
    self.ID = id
    return self