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
    return "\\\"" # Double Escaped
  
  def CloseBrackets(self):
    return "\\\"" # Double Escaped
  
  def GetParameter(self, parameterName: str = "", index: int = -1):
    return f":{parameterName}"
  
  def EndQuery(self):
    return ""
  
  def HasSchema(self):
    return False # ..
  
  def TOP(self, number):
    return f""
  
  def LIMIT(self, number):
    return f" FETCH FIRST {str(number)} ROWS ONLY"
  
  def LIMIT_OFFSET(self, limit_number, offset_number):
    return f" OFFSET {str(offset_number)} ROWS FETCH NEXT {str(limit_number)} ROWS ONLY"
  
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
  
  ##########################################################################
  # Connection
  ##########################################################################
  
  def PythonConnectionClass(self):
    return "oracledb"
  
  ##########################################################################
  # Initialize Connection
  ##########################################################################

  def CSharpInitializeConnection(self, s):
    return s
  
  def PythonInitializeConnection(self, s):

    

    connclass = self.PythonConnectionClass()
    s.wln('dsn = f"{config.Server.upper()}:{config.PortNumber}/{config.ServiceName.upper()}"')
    s.wln(f"connection = {connclass}.connect(").o()
    s.wln("user=config.Username,")
    s.wln("password=keyring.get_password(config.Credential, config.Username),")
    s.wln("dsn=dsn")
    s.c()
    s.wln(f")")
    return s
  
  def JavaInitializeConnection(self, s):
    return s 
  
  def GoInitializeConnection(self, s):
    return s
  
  def JavaScriptInitializeConnection(self, s):
    return s