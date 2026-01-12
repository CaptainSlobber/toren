from ..languages.Language import Language
from ..languages.LanguageCSharp import LanguageCSharp
from ..languages.LanguageGo import LanguageGo
from ..languages.LanguagePython import LanguagePython
from ..languages.LanguageJavaScript import LanguageJavaScript
from ..languages.LanguageJava import LanguageJava
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
    #return f"@{parameterName}"
    return f"?"
  
  def UsesNamedParameters(self, language: Language):
    _unparams = {}
    _unparams[LanguagePython().getID()] = False # pyodbc uses positional parameters with '?'
    _unparams[LanguageCSharp().getID()] = True
    _unparams[LanguageJava().getID()] = True
    _unparams[LanguageGo().getID()] = True
    _unparams[LanguageJavaScript().getID()] = True
    return _unparams[language.getID()]

  def TOP(self, number):
    return f"TOP {str(number)} "
  
  def LIMIT(self, number):
    return f""
  
  def LIMIT_OFFSET(self, limit_number, offset_number):
    return f" OFFSET {str(offset_number)} ROWS FETCH NEXT {str(limit_number)} ROWS ONLY"

  ##########################################################################
  # Dependencies
  ##########################################################################

  def CSharpDependencies(self):
    return ["using System.Data.SqlClient;"]
  
  def PythonDependencies(self):
    return ["import pyodbc"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;", "import java.sql.PreparedStatement;"]
  
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
  
  ##########################################################################
  # Initialize Connection
  ##########################################################################

  def CSharpInitializeConnection(self, s):
    return s
  
  def PythonInitializeConnection(self, s):
    connclass = self.PythonConnectionClass()
    s.wln("credential = keyring.get_password(config.Credential, config.Username)")
    s.wln("password = base64.b64decode(credential.encode('utf-8')).decode('utf-8')")
    s.wln('connectionstr= (')
    s.wln('f"DRIVER={config.Driver};"')
    s.wln('f"SERVER={config.InstanceName};"')
    s.wln('f"DATABASE={config.Database};"')
    s.wln('f"UID={config.Username};"')
    s.wln('f"PWD={password}"')
    s.wln(')')
    s.ret()

    s.wln(f"connection = {connclass}.connect(connectionstr)")
    return s
  
  def JavaInitializeConnection(self, s):
    s.wln('Base64.Decoder decoder = Base64.getDecoder();')
    s.wln('String password = new String(decoder.decode(System.getenv(config.getCredential())), StandardCharsets.UTF_8);')
    s.wln('String username = config.getUsername();')
    s.wln('String database = config.getDatabase();')
    s.wln('String instance = config.getInstanceName();')
    s.wln('int portno = config.getPortNumber();')
    s.wln('String connectionformat = "jdbc:sqlserver://%s:%d;databaseName=%s;user=%s;password=%s;encrypt=true;trustServerCertificate=true;";')
    s.wln('String connectionstr = String.format(connectionformat, instance, portno, database, username, password);')
    s.w('try ').o()
    s.wln('connection = DriverManager.getConnection(connectionstr);')
    s.b(" catch (SQLException e) ")
    s.wln("e.printStackTrace();")
    s.c()
    return s 
  
  def GoInitializeConnection(self, s):
    return s
  
  def JavaScriptInitializeConnection(self, s):
    return s