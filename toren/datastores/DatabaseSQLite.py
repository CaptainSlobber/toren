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
  
  def GetCreateForeignKeyQuery(self, schemea, table, property, foreignKey, onDeleteCascade: bool = False):

    table_name = f"{self.OB()}{table.Name}{self.CB()}"
    property_name = f"{self.OB()}{property.Name}{self.CB()}"
    foreign_table_name = f"{self.OB()}{foreignKey.FKClass.Name}{self.CB()}"
    foreign_property_name = f"{self.OB()}{foreignKey.FKClassProperty.Name}{self.CB()}"
    create_fk_query = f"FOREIGN KEY({property_name}) REFERENCES {foreign_table_name} ({foreign_property_name})"

    return create_fk_query
  
  ##########################################################################
  # Dependencies
  ##########################################################################
  
  def CSharpDependencies(self):
    return ["using Microsoft.Data.Sqlite;"]
  
  def PythonDependencies(self):
    return ["import sqlite3"]
  
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
    return "sqlite3"