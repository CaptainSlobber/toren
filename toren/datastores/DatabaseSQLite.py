from .Database import Database
import collections

class DatabaseSQLite(Database):
  
  def __init__(self):
    self.Type = "toren.datastores.DatabaseSQLite"
    self.Name = "Sqlite"
    self.Description = "Sqlite"
    self.ID = "febd77a2-29dc-44ac-8b1b-247ac6b4d45f"


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.DatabaseSQLite"
    self.Name = name
    self.Description = description
    self.ID = id
    return self

  def CSharpDependencies(self):
    return ["using Microsoft.Data.Sqlite;"]
  
  def PythonDependencies(self):
    return ["import sqlite3"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;"]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]