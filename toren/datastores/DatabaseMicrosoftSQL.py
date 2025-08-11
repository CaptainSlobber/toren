from .Database import Database
import collections

class DatabaseMicrosoftSQL(Database):


  class PropertName(Database.PropertName):
    pass

  class PropertID(Database.PropertID):
    pass
  
  def __init__(self):
    super().__init__()

  def getName(self):
    return "MSSQL"
  
  def getDescription(self):
    return "Microsoft SQL"

  def getType(self):
    return "toren.datastores.DatabaseMicrosoftSQL"
  
  def getID(self):
    return "4164e939-2725-4a26-8ae0-b28eccf0e997"

  def CSharpDependencies(self):
    return ["using System.Data.SqlClient;"]

  def PythonDependencies(self):
    return ["import pyodbc"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;"]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]