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

    
    def removeDatabase(self, key):
        if key in self.Data:
            del self.Data[key]

    def addDatabase(self, database, parentproject):
        if isinstance(database, dict): 

            databaseclassname=database["Type"].split(".")[-1]

            match databaseclassname:
                case "DatabasePostgreSQL": database = DatabasePostgreSQL().from_dict(database)
                case "DatabaseSQLite": database = DatabaseSQLite().from_dict(database)
                case "DatabaseOracle": database = DatabaseOracle().from_dict(database)
                case "DatabaseMicrosoftSQL": database = DatabaseMicrosoftSQL().from_dict(database)

        database.setParentProject(parentproject)
        self.Data[database.ID] = database

    def from_list(self, databaselist: List[Database] = [], parentproject =None):
        self.Data = collections.OrderedDict()
        if not databaselist is None:
            for database in databaselist:
                self.addDatabase(database, parentproject)
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [d.to_dict() for d in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, databases: dict, parentproject =None):
        self.Data = collections.OrderedDict()
        if not databases is None:
            for key, value in databases.items():
                self.addDatabase(value, parentproject)
        return self  
                
