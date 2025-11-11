from .Database import Database
import collections

class DatabasePostgreSQL(Database):
  
  class PropertName(Database.PropertName):
    pass

  class PropertID(Database.PropertID):
    pass
  
  def __init__(self):
    super().__init__()

  def getName(self):
    return "PostgreSQL"
  
  def getDescription(self):
    return "PostgreSQL"

  def getType(self):
    return "toren.datastores.DatabasePostgreSQL"
  
  def getID(self):
    return "be3f92e2-e2ff-491d-9ca0-eaefb72cc6bf"
  
  ##########################################################################
  # Dependencies
  ##########################################################################

  def CSharpDependencies(self):
    return ["using Npgsql;"]
  
  def PythonDependencies(self):
    return ["import psycopg2"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;"]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]
  
  ##########################################################################
  # Connection
  ##########################################################################

  def PythonConnectionClass(self):
    return "psycopg2"