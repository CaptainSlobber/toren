from .Database import Database
import collections

class DatabaseSQLite(Database):

  class PropertName(Database.PropertName):
    pass

  class PropertID(Database.PropertID):
    pass
  
  def __init__(self):
    super().__init__()

  def getName(self):
    return "Sqlite"
  
  def getDescription(self):
    return "Sqlite"

  def getType(self):
    return "toren.datastores.DatabaseSQLite"
  
  def getID(self):
    return "febd77a2-29dc-44ac-8b1b-247ac6b4d45f"
  
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