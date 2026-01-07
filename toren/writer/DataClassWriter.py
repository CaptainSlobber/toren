import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .PropertyWriter import PropertyWriter
from .StringWriter import StringWriter
from ..Project import Project
from ..datastores.Database import Database
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class DataClassWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language,
                 database: Database, 
                 dlclassname: str,
                 connectionobjectclassname: str,
                 commonfunctionsclassname: str,
                 filterobjectclassname: str,
                 logger:Logger=None,):
        super().__init__()
        self.DLCLassName = dlclassname
        self.Project = project
        self.Module = module
        self.StringWriterClass = StringWriter
        self.Class = class_
        self.Language = language
        self.Database = database
        self.ConnectionObjectClassName = connectionobjectclassname
        self.CommonFunctionsClassName = commonfunctionsclassname
        self.FilterObjectClassName = filterobjectclassname
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)

    def getParentClassName(self):
        if self.Class.InheritsFrom is not None:
            return self.Class.InheritsFrom.Name
        return ""

    def getDLDependencies(self):
        dependency_map = {}
        for propertyid, property in self.Class.Properties.Data.items():
            pass
        return dependency_map


    def writeDLDependencies(self, dependency_map, s:StringWriter):
        
        for dependencyid, dependency in dependency_map.items():
            s.wln(f"{dependency}")
        
        s.ret()
        return s
    
    def writeDLClassOpen(self, s:StringWriter):
        s.write(f"class {self.Class.Name}").o()
        s.wln(f" ")
        s.wln(f"// {self.Class.Description}")
        s.wln(f" ")
        return s
    
    def writeParentClassInitializer(self, s:StringWriter):
        return s

    def writeDLClassInitializer(self, s:StringWriter):

        s.wln("init() {}")
        return s
    
    def writeDLClassProperties(self, s:StringWriter):
        return s
    
    def writeDLClassOperations(self, s:StringWriter):

        s = self.checkTableExistence(s)
        s = self.writeCreateTable(s)
        s = self.writeDropTable(s)
        s = self.writeClearTable(s)
        s = self.writeCreateForeignKeys(s)
        s = self.writeGetColumnNames(s)
        s = self.writeGetColumnParameters(s)
        s = self.writeInsertItem(s)     
        s = self.writeInsertCollection(s)
        s = self.writeUpdate(s) 
        s = self.writeDelete(s)
        s = self.writeSelectSingleRecordByPK(s)
        s = self.writeSelectWhere(s)
        s = self.writeSelectAll(s)
        s = self.writeSelectPage(s)
        s = self.writeSelectPageWhere(s)
        s = self.writeFilterPage(s)
        return s

    def writeCreateForeignKeys(self, s:StringWriter):
        return s

    def getSchema(self):
        db = self.Database
        if db.HasSchema():
            return f"{db.OB()}{self.Class.ParentModule.Name}{db.CB()}."
        return ""

    def writeClearTable(self, s:StringWriter):
        return s

    def writeGetColumnNames(self, s:StringWriter):
        return s

    def writeGetColumnParameters(self, s:StringWriter):
        return s

    def checkTableExistence(self, s:StringWriter):
        return s
    
    def writeDropTable(self, s:StringWriter):
        return s
    
    def writeCreateTable(self, s:StringWriter):
        return s
    
    def writeInsertItem(self, s:StringWriter):
        return s
    
    def writeInsertCollection(self, s:StringWriter):
        return s
    
    def writeUpdate(self, s:StringWriter):
        return s
    
    def writeDelete(self, s:StringWriter):
        return s
    
    def writeSelectSingleRecordByPK(self, s:StringWriter):
        return s
    
    def writeSelectWhere(self, s:StringWriter):
        return s
    
    def writeSelectAll(self, s:StringWriter):
        return s
    
    def writeSelectPage(self, s:StringWriter):
        return s
    
    def writeFilterPage(self, s:StringWriter):
        return s

    def writeSelectPageWhere(self, s:StringWriter):
        return s

    def writeSelectWhere(self, s:StringWriter):
        return s

    def writeDLClassClose(self, s:StringWriter):
        s.c()
        return s
    
    def writeDLPackage(self, s:StringWriter):
        return s
    

    def write(self):
        self.writeDLClass()

    def writeDLClass(self):
        self.Logger.Log(f"  -> Writing {self.Language.Name} Class: {self.Class.Name}")
        self.S = self.StringWriterClass(self.Language)
        s = self.S
        dependencies = self.getDLDependencies()
        s = self.writeDLPackage(s)
        s = self.writeDLDependencies(dependencies, s)
        s = self.writeDLClassOpen(s)
        s = self.writeDLClassInitializer(s)
        s = self.writeDLClassProperties(s)
        s = self.writeDLClassOperations(s)
        s = self.writeDLClassClose(s)
        self.createDLClassFile(s)


    def getDLClassName(self):
        return f"{self.DLCLassName}"

    def createDLClassFile(self, s:StringWriter):

        dbmod = f"{self.Module.Name.lower()}_{self.Database.Name.lower()}"
        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                self.Project.Name, 
                                                dbmod)


        
        fn = f"{self.getDLClassName()}.{self.Language.DefaultFileExtension}"
        self.writeFile(data_module_path, fn, s.toString())