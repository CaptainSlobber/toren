from .Database import Database
import collections
from ..languages.Language import Language
from ..languages.LanguageCSharp import LanguageCSharp
from ..languages.LanguageGo import LanguageGo
from ..languages.LanguagePython import LanguagePython
from ..languages.LanguageJavaScript import LanguageJavaScript
from ..languages.LanguageJava import LanguageJava

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
  
  def GetParameter(self, language: Language, parametername:str= "", parameterNo: int= -1):
    _params = {}
    _params[LanguagePython().getID()] = f":{parametername.lower()}"
    _params[LanguageCSharp().getID()] = f":{parametername.lower()}"
    _params[LanguageJava().getID()] = f":{parametername.lower()}"
    _params[LanguageGo().getID()] = f":{parametername.lower()}"
    _params[LanguageJavaScript().getID()] = f":{parametername.lower()}"
    return _params[language.getID()]
  
  
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
    return ["using Oracle.ManagedDataAccess.Client;", "using System.Text;"] #"System.Data.OracleClient;", "using Oracle.DataAccess.Client;"
  
  def PythonDependencies(self):
    return ["import oracledb"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", "import java.sql.DriverManager;", "import java.sql.SQLException;", "import java.sql.PreparedStatement;"]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]
  
  ##########################################################################
  # Connection
  ##########################################################################
  
  def PythonConnectionClass(self):
    return "oracledb"
  
  def JavaConnectionClass(self):
    return "Connection"

  def CSharpConnectionClass(self):
    return "OracleConnection"

  ##########################################################################
  # Command
  ##########################################################################

  def CSharpCommandClass(self):
    return "OracleCommand"

  ##########################################################################
  # SQL Reader 
  ##########################################################################

  def CSharpReaderClass(self):
    return "OracleDataReader"

  ##########################################################################
  # SQL Exception 
  ##########################################################################

  def CSharpSQLExceptionClass(self):
    return "OracleException"
  
  ##########################################################################
  # Initialize Connection
  ##########################################################################

  def CSharpInitializeConnection(self, s):
    s.wln('string password = Encoding.UTF8.GetString(Convert.FromBase64String(Environment.GetEnvironmentVariable(config.Credential)));')
    s.wln('string username = config.Username;')
    s.wln('string database = config.Database;')
    s.wln('string instance = config.InstanceName;')
    s.wln('string portno = config.PortNumber.ToString();')
    s.wln('string connectionString = $"Data Source=(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST={instance})(PORT={portno})))(CONNECT_DATA=(SERVICE_NAME={database})));User Id={username};Password={password};";')
    s.wln(f"connection = new {self.CSharpConnectionClass()}(connectionString);") 
    return s
  
  def PythonInitializeConnection(self, s):

    

    connclass = self.PythonConnectionClass()
    s.wln("credential = keyring.get_password(config.Credential, config.Username)")
    s.wln("password = base64.b64decode(credential.encode('utf-8')).decode('utf-8')")
    s.wln('dsn = f"{config.Server.upper()}:{config.PortNumber}/{config.ServiceName.upper()}"')
    s.wln(f"connection = {connclass}.connect(").o()
    s.wln("user=config.Username,")
    s.wln("password=password,")
    s.wln("dsn=dsn")
    s.c()
    s.wln(f")")
    return s
  
  def JavaInitializeConnection(self, s):
    s.wln('Base64.Decoder decoder = Base64.getDecoder();')
    s.wln('String password = new String(decoder.decode(System.getenv(config.getCredential())), StandardCharsets.UTF_8);')
    s.wln('String username = config.getUsername();')
    #s.wln('String database = config.getDatabase();')
    s.wln('String server = config.getServer();')
    s.wln('String servicename = config.getServiceName();')
    s.wln('int portno = config.getPortNumber();')
    s.wln('String connectionformat = "jdbc:oracle:thin:@//%s:%d/%s";')
    s.wln('String connectionstr = String.format(connectionformat, server, portno, servicename);')
    s.w('try ').o()
    s.wln('connection = DriverManager.getConnection(connectionstr, username, password);')
    s.b(" catch (SQLException e) ")
    s.wln("e.printStackTrace();")
    s.c()
    return s 
  
  def GoInitializeConnection(self, s):
    return s
  
  def JavaScriptInitializeConnection(self, s):
    return s