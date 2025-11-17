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
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def writeDataModuleHeader(self, path, filename):
        s = self.S
        s.clear()
        con = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        s.wln(f"from .{con} import {con}")
        s.wln(f"from .{cfn} import {cfn}")
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            s.wln(f"from .{dlclassname} import {dlclassname}")
        self.writeFile(path, filename, s.toString())


    def getDataDependencies(self):
        dependency_map = {}
        for dependency in self.Database.PythonDependencies():
            dependency_map[dependency] = dependency
        return dependency_map

    def writeCommonDataFunctions(self, path, classname):
        s = self.S
        s.clear()
        
        

        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        dependency_map = self.getDataDependencies()
        s = self.writeDataDependencies(dependency_map, s)

        s.wln(f"from .{conclass} import {conclass}")
        s.ret()
        s.write(f"class {classname}():").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Datalayer Functions")
        s.wln("\"\"\"")
        s.ret()

        s = self.writeCommonCreateConnection(s)
        s = self.writeCommonExecuteNonQuery(s)
        s = self.writeCommonExecuteParameterizedNonQuery(s)
        s = self.writeCommmonFetchOne(s)
        s = self.writeCommonFetchAll(s)

        filename = f"{classname}.{self.Language.DefaultFileExtension}"
        self.writeFile(path, filename, s.toString())

    
    def writeCommonCreateConnection(self, s:PythonStringWriter):
        db = self.Database
        conclass = self.ConnectionObjectClassName

        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        s.wln(f"@staticmethod")
        s.wln(f"def GetConnection(c: {conclass}):").o()

        s.wln(f"connection = {db.ConnectionClass(self.Language)}.connect(").o()
        s.c()
        s.wln(f")")
        s.wln(f"return connection")
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

    def writeCommonExecuteParameterizedNonQuery(self, s:PythonStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteParameterizedNonQuery(connection, query: str, data: dict, close: bool=True):").o()
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.execute(query, data)")
        s.wln(f"connection.commit()") 
        s = self.writeCommonCleanupConnection(s)
        s.c()
        s.ret()

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteManyParameterizedNonQuery(connection, query: str, data: list, close: bool=True):").o()
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

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteFetchOne(connection, query: str, data: dict, close: bool=True) -> dict:").o()
        s.wln("result = {}")
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.execute(query, data)")
        s.wln(f"row = cursor.fetchone()") 
        s.wln(f"column_names = [description[0] for description in cursor.description]")
        s.wln(f"if row is not None:").o()
        s.wln(f"result = dict(zip(column_names, row))")
        s.c()
        
        s = self.writeCommonCleanupConnection(s)
        s.wln(f"return result")
        s.c()
        s.ret()
        return s
    
    def writeCommonFetchAll(self, s:PythonStringWriter): 
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteFetchAll(connection, query: str, data: dict, close: bool=True) -> list:").o()
        s.wln(f"results = []")
        s.wln(f"try:").o()
        s.wln(f"cursor = connection.cursor()")
        s.wln(f"cursor.execute(query, data)")
        s.wln(f"rows = cursor.fetchall()") 
        s.wln(f"column_names = [description[0] for description in cursor.description]")
        s.wln(f"for row in rows:").o()      
        s.wln(f"result = dict(zip(column_names, row))")
        s.wln(f"results.append(result)")
        
        s = self.writeCommonCleanupConnection(s)
        s.wln(f"return results")
        s.c()
        s.ret()
        return s
    
    def writeCommonExecuteNonQuery(self, s:PythonStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteNonQuery(connection, query: str, close: bool=True):").o()
        s.wln(f"return {cfn}.ExecuteNonQueries(connection, [query], close)")
        s.c()
        s.ret()

        s.wln(f"@staticmethod")
        s.wln(f"def ExecuteNonQueries(connection, queries: list, close: bool=True):").o()
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