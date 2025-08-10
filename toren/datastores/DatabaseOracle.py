from .Database import Database
import collections

class DatabaseOracle(Database):
  
  def __init__(self):
    self.Type = "toren.datastores.DatabaseOracle"
    self.Name = "Oracle"
    self.Description = "Oracle"
    self.ID = "1a188e6f-f5d3-4f18-9e19-7cbfb3eb7d42"


  def initialize(self, name: str, 
                 description: str, 
                 id: str):
    self.Type = "toren.datastores.DatabaseOracle"
    self.Name = name
    self.Description = description
    self.ID = id
    return self
  
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