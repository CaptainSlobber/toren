from .Database import Database
import collections

class DatabaseSQLite(Database):

  class PropertName(Database.PropertName):
    pass

  class PropertID(Database.PropertID):
    pass
  
  def __init__(self):
    super().__init__()

  def getName(self):
    return "Sqlite"
  
  def getDescription(self):
    return "Sqlite"

  def getType(self):
    return "toren.datastores.DatabaseSQLite"
  
  def getID(self):
    return "febd77a2-29dc-44ac-8b1b-247ac6b4d45f"
  
  ##########################################################################
  # DB Specific Query Syntax
  ##########################################################################

  def HasSchema(self):
    return False
  
  # SQLite parameters can be prefixed with either :, @, or $.
  def GetParameter(self, parameterName: str = "", index: int = -1):
    return f"@{parameterName}"
  
  def SeparateForeignKeyCreation(self):
    return False
  
  def GetCreateForeignKeyQuery(self, schema, table, property, foreignKey, onDeleteCascade: bool = False):

    table_name = self.GetTableName(table)
    schema_name = f"{self.OB()}{schema}{self.CB()}"
    property_name = f"{self.OB()}{property.Name}{self.CB()}"
    foreign_table_name = self.GetTableName(foreignKey.FKClass)

    foreign_property_name = f"{self.OB()}{foreignKey.FKClassProperty.Name}{self.CB()}"
    create_fk_query = f"FOREIGN KEY({property_name}) REFERENCES {foreign_table_name} ({foreign_property_name})"

    return create_fk_query
  
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
    return ["using Microsoft.Data.Sqlite;"]
  
  def PythonDependencies(self):
    return ["import sqlite3"]
  
  def JavaDependencies(self):
    return ["import java.sql.Connection;", 
            "import java.sql.DriverManager;", 
            "import java.sql.SQLException;", 
            "import java.sql.PreparedStatement;"]
  
  def GoDependencies(self):
    return [""]
  
  def JavaScriptDependencies(self):
    return [""]
  
  ##########################################################################
  # Connection
  ##########################################################################

  def PythonConnectionClass(self):
    return "sqlite3"
  
  def JavaConnectionClass(self):
    return "Connection"
  
  ##########################################################################
  # Initialize Connection
  ##########################################################################

  def CSharpInitializeConnection(self, s):
    return s
  
  def PythonInitializeConnection(self, s):
    connclass = self.PythonConnectionClass()
    #s.wln("credential = keyring.get_password(config.Credential, config.Username)")
    #s.wln("password = base64.b64decode(credential.encode('utf-8')).decode('utf-8')")
    s.wln(f"connection = {connclass}.connect(config.DataPath)")
    return s
  
  def JavaInitializeConnection(self, s):
    
    s.wln('String datapath = config.getDataPath();')
    s.wln('String connectionformat = "jdbc:sqlite:%s";')
    s.wln('String connectionstr = String.format(connectionformat, datapath);')
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