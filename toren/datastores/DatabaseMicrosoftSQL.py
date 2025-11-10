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
  
  ##########################################################################
  # DB Specific Query Syntax
  ##########################################################################

  def IfNotExists(self):
    return ""

  ##########################################################################
  # Dependencies
  ##########################################################################

  def CSharpDependencies(self):
    return ["using System.Data.SqlClient;"]
  
  def CSharpConnectionClass(self):
    return "SqlConnection"

  def PythonDependencies(self):
    return ["import pyodbc"]
  
  def PythonConnectionClass(self):
    return "pyodbc"
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;"]
  
  def JavaConnectionClass(self):
    return "Connection"

  def GoDependencies(self):
    return [""]
  
  def GoConnectionClass(self):
    return ""
  
  def JavaScriptDependencies(self):
    return [""]
  
  def JavaScriptConnectionClass(self):
    return ""