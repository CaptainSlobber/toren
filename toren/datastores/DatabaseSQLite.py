from .Database import Database
import collections

class DatabaseSQLite(Database):
  
  def __init__(self, name: str, description: str, id: str):
    self.Name = name
    self.Description = description
    self.ID = id
