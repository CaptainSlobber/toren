from .Database import Database
import collections

class DatabaseOracle(Database):

  class PropertName(Database.PropertName):
    pass

  class PropertID(Database.PropertID):
    pass
  
  def __init__(self):
    super().__init__()

  def getName(self):
    return "Oracle"
  
  def getDescription(self):
    return "Oracle"

  def getType(self):
    return "toren.datastores.DatabaseOracle"
  
  def getID(self):
    return "1a188e6f-f5d3-4f18-9e19-7cbfb3eb7d42"
  
  ##########################################################################
  # DB Specific Query Syntax
  ##########################################################################

  def OpenBrackets(self):
    return "\""
  
  def CloseBrackets(self):
    return "\""
  
  ##########################################################################
  # Dependencies
  ##########################################################################

  def CSharpDependencies(self):
    return ["using Oracle.DataAccess.Client;", "using Oracle.ManagedDataAccess.Client;"] #System.Data.OracleClient
  
  def PythonDependencies(self):
    return ["import oracledb"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;"]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]