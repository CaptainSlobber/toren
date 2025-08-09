from .Database import Database
import collections

class DatabasePostgreSQL(Database):
  
  def __init__(self):
    self.Type = "toren.datastores.DatabasePostgreSQL"
    self.Name = "PostgreSQL"
    self.Description = "PostgreSQL"
    self.ID = "be3f92e2-e2ff-491d-9ca0-eaefb72cc6bf"


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.DatabasePostgreSQL"
    self.Name = name
    self.Description = description
    self.ID = id
    return self