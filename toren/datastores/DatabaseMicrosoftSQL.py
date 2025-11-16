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

  # Note: The IF EXISTS clause for DROP TABLE is supported in SQL Server 2016 and later versions. 
  # For older versions, alternative methods like checking OBJECT_ID or INFORMATION_SCHEMA.TABLES are required.

  def IfNotExists(self):
    return ""
  
  def IfExists(self):
    return " IF EXISTS"
  
  def GetParameter(self, parameterName: str = "", index: int = -1):
    return f"@{parameterName}"

  ##########################################################################
  # Dependencies
  ##########################################################################

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

  ##########################################################################
  # Connection
  ##########################################################################

  def CSharpConnectionClass(self):
    return "SqlConnection"
  
  def PythonConnectionClass(self):
    return "pyodbc"
  
  def JavaConnectionClass(self):
    return "Connection"
  
  def GoConnectionClass(self):
    return ""
    
  def JavaScriptConnectionClass(self):
    return ""