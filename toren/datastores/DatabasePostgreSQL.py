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
  # DB Specific Query Syntax
  ##########################################################################
  
  def GetParameter(self, parameterName: str = "", index: int = -1):
    return f"%({parameterName})s"
  
  def OpenBrackets(self):
    return ""
  
  def CloseBrackets(self):
    return ""
  
  
  def OpenBrackets(self):
    return "\\\"" # Double Escaped
  
  def CloseBrackets(self):
    return "\\\"" # Double Escaped
  
  def TOP(self, number):
    return f""
  
  def LIMIT(self, number):
    return f" LIMIT {str(number)}"
  
  def OFFSET(self, number):
    return f" OFFSET {str(number)}"
  
  def LIMIT_OFFSET(self, limit_number, offset_number):
    return f" LIMIT {str(limit_number)} OFFSET {str(offset_number)}"
  
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
  
  def JavaConnectionClass(self):
    return "Connection"
  
  ##########################################################################
  # Initialize Connection
  ##########################################################################

  def CSharpInitializeConnection(self, s):
    return s
  
  def PythonInitializeConnection(self, s):
    connclass = self.PythonConnectionClass()
    s.wln(f"connection = {connclass}.connect(").o()
    s.wln("user=config.Username,")
    s.wln("password=keyring.get_password(config.Credential, config.Username),")
    s.wln("host=config.Server,")
    s.wln("port=config.PortNumber,")
    s.wln("database=config.Database")
    s.c()
    s.wln(f")")
    return s
  
  def JavaInitializeConnection(self, s):
    return s 
  
  def GoInitializeConnection(self, s):
    return s
  
  def JavaScriptInitializeConnection(self, s):
    return s