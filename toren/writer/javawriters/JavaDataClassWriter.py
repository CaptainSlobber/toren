import collections
import json
import os
from pathlib import Path

from typing import List
from ..DataClassWriter import DataClassWriter
from .JavaStringWriter import JavaStringWriter
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class JavaDataClassWriter(DataClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 database: Database,
                 dlclassname: str,
                 connectionobjectclassname: str,
                 commonfunctionsclassname: str,
                 filterobjectclassname: str,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         database=database,
                         language=language,
                         dlclassname=dlclassname, 
                         connectionobjectclassname=connectionobjectclassname,
                         commonfunctionsclassname=commonfunctionsclassname,
                         filterobjectclassname=filterobjectclassname,
                         logger=logger)
        self.Project = project
        self.Module = module
        self.StringWriterClass = JavaStringWriter
        self.Class = class_
        self.DLCLassName = dlclassname
        self.ConnectionObjectClassName = connectionobjectclassname
        self.CommonFunctionsClassName = commonfunctionsclassname
        self.FilterObjectClassName = filterobjectclassname
        self.Database = database
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)

    def getDLDependencies(self):
        dependency_map = {}
        for dependency in self.Database.JavaDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        

        return dependency_map
    
    def writeDLPackage(self, s:JavaStringWriter):
        p = self.Class.ParentModule.ParentProject.Name.lower()
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name.lower()
        b = self.Database.Name.lower()
        t = self.Class.ParentModule.ParentProject.TLD.lower()
        s.wln(f"package {t}.{e}.{p}.{m}.{b};")
        s.ret()
        return s
    
    def getDataModulePath(self):
        return self.getParentModulePath()

    def getParentModulePath(self):
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD.lower()
        src = "src"
        main = "main"
        java = "java"
        dbmod = f"{m}.{b}"

        data_module_path = os.path.join(self.Language.OutputDirectory,p, dbmod, src, main, java, t, e, p, m, b)
        return data_module_path

    def writeDLClassOpen(self, s:JavaStringWriter):

        
        c = self.Class.Name
        d = self.getDLClassName()
        
        s.ret()
        s.write(f"public class {d} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" {self.Database.Name} Data Layer for Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("*/")
        s.ret()
        return s
    
    def writeParentClassInitializer(self, s:JavaStringWriter):
        return s

    def writeDLClassInitializer(self, s:JavaStringWriter):
        #d = self.getDLClassName()
        #s.wln(f"public {d}() {{}}")
        #s.ret()
        return s
    
    def writeDLClassProperties(self, s:JavaStringWriter):
        s.wln(f"public static String SCHEMA_NAME = \"{self.Class.ParentModule.Name}\";")
        s.wln(f"public static String TABLE_NAME = \"{self.Class.Name}\";")
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s.wln(f"public static String COL_NAME_{property.Name.upper()} = \"{property.Name}\";")
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"public static String COL_NAME_{property.Name.upper()} = \"{property.Name}\";")
        s.ret()
        return s
    

    def writeCreateTableColumn(self, s:JavaStringWriter, property):
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
        
        s.wln(f'createquery += "{db.OB()}{property.Name}{db.CB()} {DATATYPE}{NOTNULL}{UNIQUE}{PRIMARYKEY},";')
        return s


  

    
    def writeCreateTable(self, s:JavaStringWriter):
        db = self.Database
        

        s.w(f"private static String create{self.Class.Name}TableQuery ()").o()
        s.wln(f'String createquery = "CREATE TABLE{db.IfNotExists()} {db.OB()}{self.Class.Name}{db.CB()} (";')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s = self.writeCreateTableColumn(s, property)
        for propertyid, property in self.Class.Properties.Data.items():
            s = self.writeCreateTableColumn(s, property)
        s.wln(f'createquery += "){db.EndQuery()}";')
        s.wln("return createquery;")
        s.c().ret()

        s.w(f"public static void create{self.Class.Name}Table () ").o()

        s.c()
        return s
    
    def writeInsert(self, s:JavaStringWriter):
        return s
    
    def writeInsertCollection(self, s:JavaStringWriter):
        return s
    
    def writeUpdate(self, s:JavaStringWriter):
        return s
    
    def writeDelete(self, s:JavaStringWriter):
        return s
    
    def writeSelectSingleRecordByPK(self, s:JavaStringWriter):
        return s
    
    def writeSelectWhere(self, s:JavaStringWriter):
        return s

    def writeDLClassClose(self, s:JavaStringWriter):
        s.c()
        return s