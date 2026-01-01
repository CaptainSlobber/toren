import collections
import json
import os
from pathlib import Path

from typing import List
from ...datastores.Database import Database
from ..DataModuleWriter import DataModuleWriter
from .PythonDataClassWriter import PythonDataClassWriter
from .PythonStringWriter import PythonStringWriter
from .PythonClassWriter import PythonClassWriter
from ...Project import Project
from ...Module import Module

from ...languages import *
from ...tracer.Logger import Logger

class PythonDataModuleWriter(DataModuleWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         language=language, 
                         database=database,
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Language = language
        self.Database = database
        self.ClassWriterClass = PythonClassWriter
        self.DataClassWriterClass = PythonDataClassWriter
        self.StringWriterClass = PythonStringWriter
        self.HeaderFileName = "__init__"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.AdminFunctionsClassName = "Admin"
        self.FilterObjectClassName = "Filter"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def writeDataModuleHeader(self, path, filename):
        s = self.S
        s.clear()
        con = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        afn = f"{self.getDLPrefix()}{ self.AdminFunctionsClassName}{self.getDLSuffix()}"
        fon = f"{self.getDLPrefix()}{ self.FilterObjectClassName}{self.getDLSuffix()}"

        s.wln(f"from .{con} import {con}")
        s.wln(f"from .{cfn} import {cfn}")
        s.wln(f"from .{afn} import {afn}")
        s.wln(f"from .{fon} import {fon}")
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            s.wln(f"from .{dlclassname} import {dlclassname}")
        self.writeFile(path, filename, s.toString())


    def getDataDependencies(self):
        dependency_map = {}
        for dependency in self.Database.PythonDependencies():
            dependency_map[dependency] = dependency
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            class_dep = f"from .{dlclassname} import {dlclassname}"
            #dependency_map[class_dep] = class_dep
        
        return dependency_map

    

    def writeOpenCommonDataFunctions(self, classname: str, s:PythonStringWriter):
        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        s.wln(f"import keyring")
        s.wln(f"import os")
        s.wln(f"from .{conclass} import {conclass}")
        s.ret()
        s.write(f"class {classname}():").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Datalayer Functions")
        s.wln("\"\"\"")
        s.ret()
        return s

    def writeOpenCommonAdminFunctions(self, classname: str, s:PythonStringWriter):
        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            class_dep = f"from .{dlclassname} import {dlclassname}"
            s.wln(class_dep)    
        s.wln(f"from .{cfn} import {cfn}")
        s.wln(f"from .{conclass} import {conclass}")
        s.ret()
        s.write(f"class {classname}():").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Admin Datalayer Functions")
        s.wln("\"\"\"")
        s.ret()
        return s
    
    def writeCommonCreateConnection(self, s:PythonStringWriter):
        db = self.Database
        conclass = self.ConnectionObjectClassName
        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        s.wln(f"@staticmethod")
        s.wln(f"def GetConnection(config: {conclass}):").o()
        s = db.WriteConnectionInitialization(self.Language, s)    
        s.wln("return connection")
        s.c()
        s.ret()
        return s
    
    def writeCommonCleanupConnection(self, s:PythonStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        s.c()
        s.wln(f"except Exception as e:").o()
        s.wln(f"connection.rollback() # Rollback changes")
        s.wln(f"#TODO: Log data error")
        s.wln(f"print(f'Database error: {{e}}')")
        s.c()
        s.wln(f"finally:").o()
        s.wln(f"if 'cursor' in locals() and cursor:").o()
        s.wln("cursor.close()")
        s.c()
        s.wln(f"if close:").o()
        s.wln(f"if 'connection' in locals() and connection:").o()
        s.wln(f"connection.close()")
        s.c().c()
        s.c()
        #s.c()
        #s.ret()
        return s
    
    def writeCommonSetupConnection(self, s:PythonStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        s.wln(f"connection = {cfn}.GetConnection(config)")
        s.ret()
        return s
    
    def getDefaultCloseConnectionParameter(self):
        return "close: bool=True"

    def writeCommonExecuteParameterizedNonQuery(self, s:PythonStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        cc  =self.getDefaultCloseConnectionParameter()
        data_data_type = "dict"
        if not db.UsesNamedParameters(self.Language):
            data_data_type = "list"

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteParameterizedNonQuery(config, query: str, data: {data_data_type}, {cc}):").o()
        s = self.writeCommonSetupConnection(s)
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.execute(query, data)")
        s.wln(f"connection.commit()") 
        s = self.writeCommonCleanupConnection(s)
        s.c()
        s.ret()

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteManyParameterizedNonQuery(config, query: str, data: {data_data_type}, {cc}):").o()
        s = self.writeCommonSetupConnection(s)
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.executemany(query, data)")
        s.wln(f"connection.commit()") 
        s = self.writeCommonCleanupConnection(s)
        s.c()
        s.ret()
        return s
    
    def writeCommmonFetchOne(self, s:PythonStringWriter):   
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        cc  =self.getDefaultCloseConnectionParameter()
        data_data_type = "dict"
        if not db.UsesNamedParameters(self.Language):
            data_data_type = "list"

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteFetchOne(config, query: str, data: {data_data_type}, translation, {cc}) -> dict:").o()
        s = self.writeCommonSetupConnection(s)
        s.wln("result = {}")
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.execute(query, data)")
        s.wln(f"row = cursor.fetchone()") 
        s.wln(f"column_names = [description[0] for description in cursor.description]")
        s.wln(f"if row is not None:").o()
        s.wln(f"_result = dict(zip(column_names, row))")
        s.wln(f"result = translation(_result)")
        s.c()
        
        s = self.writeCommonCleanupConnection(s)
        s.wln(f"return result")
        s.c()
        s.ret()
        return s
    
    def writeCommonFetchAll(self, s:PythonStringWriter): 
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        cc  =self.getDefaultCloseConnectionParameter()
        data_data_type = "dict"
        if not db.UsesNamedParameters(self.Language):
            data_data_type = "list"
        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteFetchAll(config, query: str, data: {data_data_type}, translation, {cc}) -> list:").o()
        s = self.writeCommonSetupConnection(s)
        s.wln(f"results = []")
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.execute(query, data)")
        s.wln(f"rows = cursor.fetchall()") 
        s.wln(f"column_names = [description[0] for description in cursor.description]")
        s.wln(f"for row in rows:").o()      
        s.wln(f"_result = dict(zip(column_names, row))")
        s.wln(f"result = translation(_result)")
        s.wln(f"results.append(result)")
        s.c()
        
        s = self.writeCommonCleanupConnection(s)
        s.wln(f"return results")
        s.c()
        s.ret()
        return s
    
    def writeCommonExecuteNonQuery(self, s:PythonStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        cc  =self.getDefaultCloseConnectionParameter()
        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteNonQuery(config, query: str, {cc}):").o()
        s.wln(f"return {cfn}.ExecuteNonQueries(config, [query], close)")
        s.c()
        s.ret()

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteNonQueries(config, queries: list, {cc}):").o()
        s = self.writeCommonSetupConnection(s)
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"for query in queries:").o()
        s.wln(f"cursor.execute(query)")
        s.wln(f"connection.commit()") 
        s.c()
        s = self.writeCommonCleanupConnection(s)
        s.c()
        s.ret()
        return s
    
    def writeCreateSchema(self, s:PythonStringWriter):
        db = self.Database
        schema_name = self.Module.Name
        afn = f"{self.getDLPrefix()}{ self.AdminFunctionsClassName}{self.getDLSuffix()}"
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        if db.HasSchema():
            s.wln("@staticmethod")
            s.wln(f"def GetCreateSchemaQuery():").o()
            s.wln(f'createquery = "CREATE SCHEMA {db.OB()}{schema_name}{db.CB()}{db.EndQuery()}"')
            s.wln("return createquery")
            s.c().ret()

            s.wln("@staticmethod")
            s.wln(f"def CreateSchema(config):").o()
            s.wln(f"createquery = {afn}.GetCreateSchemaQuery()")
            s.wln(f"{cfn}.ExecuteNonQuery(config, createquery)")
            s.c()
            s.ret()

        return s
    
    def writeCheckSchemaExistence(self, s:PythonStringWriter):
        db = self.Database
        schema_name = self.Module.Name
        afn = f"{self.getDLPrefix()}{ self.AdminFunctionsClassName}{self.getDLSuffix()}"

        if db.HasSchema():
            s.wln("@staticmethod")
            s.wln(f"def CheckSchemaExistence(config) -> bool:").o()
            s.wln("return False") # TODO
            s.c()
            s.ret()

        return s
    
    
    def writeDropAllTables(self, s:PythonStringWriter):
        s.wln("@staticmethod")
        s.wln(f"def DropAllTables(config):").o()
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            s.wln(f"{dlclassname}.Drop{_class.Name}Table(config)")
        s.c()
        s.ret()
        return s
    
    def writeClearAllTables(self, s:PythonStringWriter):
        s.wln("@staticmethod")
        s.wln(f"def ClearAllTables(config):").o()
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            s.wln(f"{dlclassname}.Clear{_class.Name}Table(config)")
        s.c()
        s.ret()
        return s
    
    def writeCreateAllTables(self, s:PythonStringWriter):
        db = self.Database
        schema_name = self.Module.Name
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        afn = f"{self.getDLPrefix()}{ self.AdminFunctionsClassName}{self.getDLSuffix()}"
        s.wln("@staticmethod")
        s.wln(f"def CreateAllTables(config):").o()
        if db.HasSchema():
            s.wln(f"{afn}.CreateSchema(config)")

            
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            s.wln(f"{dlclassname}.Create{_class.Name}Table(config)")
        s.wln("")
        if db.SeparateForeignKeyCreation():
            for classid, _class in self.Module.Classes.Data.items():
                dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
                s.wln(f"{dlclassname}.Create{_class.Name}ForeignKeys(config)")
        s.c()
        s.ret()
        return s