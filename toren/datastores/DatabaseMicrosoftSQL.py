from .Database import Database
import collections

class DatabaseMicrosoftSQL(Database):
  
  def __init__(self):
    self.Type = "toren.datastores.DatabaseMicrosoftSQL"
    self.Name = "MSSQL"
    self.Description = "Microsoft SQL"
    self.ID = "4164e939-2725-4a26-8ae0-b28eccf0e997"


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.DatabaseMicrosoftSQL"
    self.Name = name
    self.Description = description
    self.ID = id
    return self