import collections
import json
import os
from pathlib import Path

from typing import List
from ..DataClassWriter import DataClassWriter
from .PythonStringWriter import PythonStringWriter
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class PythonDataClassWriter(DataClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 database: Database,
                 dlclassname: str,
                 connectionobjectclassname: str,
                 commonfunctionsclassname: str,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         database=database,
                         language=language,
                         dlclassname=dlclassname, 
                         connectionobjectclassname=connectionobjectclassname,
                         commonfunctionsclassname=commonfunctionsclassname,
                         logger=logger)
        self.Project = project
        self.Module = module
        self.StringWriterClass = PythonStringWriter
        self.Class = class_
        self.DLCLassName = dlclassname
        self.ConnectionObjectClassName = connectionobjectclassname
        self.CommonFunctionsClassName = commonfunctionsclassname
        self.Database = database
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)



    def getDLDependencies(self):
        dependency_map = {}
        for dependency in self.Database.PythonDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        

        return dependency_map

    def writeDLClassOpen(self, s:PythonStringWriter):

        p = self.Class.ParentModule.ParentProject.Name
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name
        b = self.Database.Name.lower()
        c = self.Class.Name
        d = self.getDLClassName()

        con = self.ConnectionObjectClassName
        cfn = self.CommonFunctionsClassName
        s.wln(f"from .{con} import {con}")
        s.wln(f"from .{cfn} import {cfn}")
        s.ret()
        s.write(f"class {d}:").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" {self.Database.Name} Data Layer for Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("\"\"\"")
        s.ret()

        return s
    
    def writeParentClassInitializer(self, s:PythonStringWriter):
        return s

    def writeDLClassInitializer(self, s:PythonStringWriter):
        d = self.getDLClassName()
        s.wln("def __init__(self):").o()
        s.wln(f"pass")
        s.c()
        s.ret()
        return s
    
    def writeDLClassProperties(self, s:PythonStringWriter):
        s.wln(f'SCHEMA_NAME = "{self.Class.ParentModule.Name}"')
        s.wln(f'TABLE_NAME = "{self.Class.Name}"')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f'COL_NAME_{property.Name.upper()} = "{property.Name}"')
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f'COL_NAME_{property.Name.upper()} = "{property.Name}"')
        s.ret()
        return s
    

    def writeCreateTableColumn(self, s:PythonStringWriter, property):
        db = self.Database
        NOTNULL = " NOT NULL"
        if property.AllowNulls:
            NOTNULL = ""
        PRIMARYKEY = ""
        if property.IsPrimaryKey: 
            PRIMARYKEY = " PRIMARY KEY"
        UNIQUE = ""
        if property.IsUnique:
            UNIQUE = " UNIQUE"
        DATATYPE = property.DatabasePropertyType(db)
        
        s.wln(f'createquery += "{db.OB()}{property.Name}{db.CB()} {DATATYPE}{NOTNULL}{UNIQUE}{PRIMARYKEY},"')
        return s


    def writeCreateSchema(self, s:PythonStringWriter):
        db = self.Database
        schema_name = self.Class.ParentModule.Name
        if db.HasSchema():
            s.wln("@staticmethod")
            s.wln(f"def CreateSchemaQuery():").o()
            s.wln(f'createquery = "CREATE SCHEMA {db.OB()}{schema_name}{db.CB()}{db.EndQuery()}"')
            s.wln("return createquery")
            s.c().ret()

            s.wln("@staticmethod")
            s.wln(f"def CreateSchema(conn):").o()
            s.wln(f"createquery = {self.getDLClassName()}.CreateSchemaQuery()")
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(conn, createquery)")
            s.c()
            s.ret()

        return s
    
    def getSchema(self):
        db = self.Database
        if db.HasSchema():
            return f"{db.OB()}{self.Class.ParentModule.Name}{db.CB()}."
        return ""

    def writeCreateTable(self, s:PythonStringWriter):
        db = self.Database
        schema = self.getSchema()

        s.wln("@staticmethod")
        s.wln(f"def Create{self.Class.Name}TableQuery():").o()
        s.wln(f'createquery = "CREATE TABLE{db.IfNotExists()} {schema}{db.OB()}{self.Class.Name}{db.CB()} ("')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s = self.writeCreateTableColumn(s, property)
        for propertyid, property in self.Class.Properties.Data.items():
            s = self.writeCreateTableColumn(s, property)
        s.wln(f'createquery += "){db.EndQuery()}"')
        s.wln("return createquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def Create{self.Class.Name}Table(conn):").o()
        s.wln(f"createquery = {self.getDLClassName()}.Create{self.Class.Name}TableQuery()")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(conn, createquery)")
        s.c()
        s.ret()
        return s
    
    def checkTableExistence(self, s:PythonStringWriter):
        return s
    
    def writeDropTable(self, s:PythonStringWriter):
        db = self.Database
        schema = self.getSchema()
        s.wln("@staticmethod")
        s.wln(f"def Drop{self.Class.Name}TableQuery():").o()
        s.wln(f'dropquery = "DROP TABLE{db.IfExists()} {schema}{db.OB()}{self.Class.Name}{db.CB()}{db.EndQuery()}"')
        s.wln("return dropquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def Drop{self.Class.Name}Table(conn):").o()
        s.wln(f"dropquery = {self.getDLClassName()}.Drop{self.Class.Name}TableQuery()")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(conn, dropquery)")
        s.c()
        s.ret()
        return s
    
    def writeGetColumnNames(self, s:PythonStringWriter):
        db = self.Database
        columns = []
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        for propertyid, property in self.Class.Properties.Data.items():
            columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        columns_string = ", ".join(columns)
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}ColumnNames():").o()
        s.wln(f'columns = "{columns_string}"')
        s.wln("return columns")
        s.c()
        s.ret()
        return s
    

    
    def writeGetColumnParameters(self, s:PythonStringWriter):
        db = self.Database
        params = []
        n = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                n = n + 1
                params.append(f"{db.GetParameter(n, property.Name.lower())}")
        for propertyid, property in self.Class.Properties.Data.items():
            n = n + 1
            params.append(f"{db.GetParameter(n, property.Name.lower())}")
        params_string = ", ".join(params)
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}ColumnParameters():").o()
        s.wln(f'params = "{params_string}"')
        s.wln("return params")
        s.c()
        s.ret()
        return s
    
    def writeInsertItem(self, s:PythonStringWriter):

        db = self.Database
        schema = self.getSchema()
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}InsertQuery():").o()
        s.wln(f'columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()')
        s.wln(f"params = {self.getDLClassName()}.Get{self.Class.Name}ColumnParameters()")
        s.wln(f'insertquery = f"INSERT INTO {schema}{db.OB()}{self.Class.Name}{db.CB()} ({{columns}}) VALUES ({{params}}){db.EndQuery()}"')
        s.wln("return insertquery")
        s.c().ret()
        return s
    
    def writeInsertCollection(self, s:PythonStringWriter):
        return s
    
    def writeUpdate(self, s:PythonStringWriter):
        return s
    
    def writeDelete(self, s:PythonStringWriter):
        return s
    
    def writeSelectSingleRecordByPK(self, s:PythonStringWriter):
        return s
    
    def writeSelectWhere(self, s:PythonStringWriter):
        return s

    def writeDLClassClose(self, s:PythonStringWriter):
        s.c()
        return s
