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


    
    def writeCreateTable(self, s:PythonStringWriter):
        db = self.Database
        s.wln("@staticmethod")
        s.wln(f"def create{self.Class.Name}TableQuery():").o()
        s.wln(f'createquery = "CREATE TABLE{db.IfNotExists()} {db.OB()}{self.Class.Name}{db.CB()} ("')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s = self.writeCreateTableColumn(s, property)
        for propertyid, property in self.Class.Properties.Data.items():
            s = self.writeCreateTableColumn(s, property)
        s.wln(f'createquery += "){db.EndQuery()}"')
        s.wln("return createquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def create{self.Class.Name}Table(conn):").o()
        s.wln(f"create_query = {self.getDLClassName()}.create{self.Class.Name}TableQuery()")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(conn, create_query)")
        s.c()
        s.ret()
        return s
    
    def writeInsert(self, s:PythonStringWriter):
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
