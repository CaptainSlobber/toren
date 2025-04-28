from ..TorenObject import TorenObject
from .Database import Database
from .DatabasePostgreSQL import DatabasePostgreSQL
from .DatabaseSQLite import DatabaseSQLite
from .DatabaseOracle import DatabaseOracle
from .DatabaseMicrosoftSQL import DatabaseMicrosoftSQL
import collections
import json
from typing import List


class DatabaseCollection():

    def getType(self):
        return "toren.datastores.DatabaseCollection"
    
    def __init__(self):
        self.Data = collections.OrderedDict()

    
    def initialize(self, databaselist: List[Database] = [], parentproject = None):
        self.from_list(databaselist, parentproject)
        return self

    
    def addDatabase(self, database, databasecollection, parentproject):
        if isinstance(database, dict): 

            databaseclassname=database["Type"].split(".")[-1]

            match databaseclassname:
                case "DatabasePostgreSQL": database = DatabasePostgreSQL().from_dict(database)
                case "DatabaseSQLite": database = DatabaseSQLite().from_dict(database)
                case "DatabaseOracle": database = DatabaseOracle().from_dict(database)
                case "DatabaseMicrosoftSQL": database = DatabaseMicrosoftSQL().from_dict(database)

        database.setParentProject(parentproject)
        databasecollection[database.ID] = database
        return databasecollection

    def from_list(self, databaselist: List[Database] = [], parentproject =None):
        _databases = collections.OrderedDict()
        if not databaselist is None:
            for database in databaselist:
                _databases = self.addDatabase(database, _databases, parentproject)
        self.Data = _databases
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [d.to_dict() for d in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, databases: dict, parentproject =None):
        _databases = collections.OrderedDict()
        if not databases is None:
            for key, value in databases.items():
                _databases = self.addDatabase(value, _databases, parentproject)
        self.Data = _databases
        return self  
                
