import collections
import json
import os
from pathlib import Path

from typing import List
from ..DataClassWriter import DataClassWriter
from .CSharpStringWriter import CSharpStringWriter
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class CSharpDataClassWriter(DataClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         database=database,
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.StringWriterClass = CSharpStringWriter
        self.Class = class_
        self.Database = database
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)

    def getDLDependencies(self):
        dependency_map = {}
        for dependency in self.Database.CSharpDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        

        return dependency_map

    def writeDLClassOpen(self, s:CSharpStringWriter):

        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        b = self.Database.Name.lower()
        l = self.getDatalayerName()
        c = self.Class.Name
        d = self.getDLClassName()
        s.wln(f"namespace {p}.{m}.{b};")
        s.ret()
        s.write(f"public class {d} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" {self.Database.Name} Data Layer for Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("*/")
        s.ret()
        return s
    
    def writeParentClassInitializer(self, s:CSharpStringWriter):
        return s

    def writeDLClassInitializer(self, s:CSharpStringWriter):
        d = self.getDLClassName()
        s.wln(f"public {d}() {{}}")
        return s
    
    
    def writeCreateTable(self, s:CSharpStringWriter):
        return s
    
    def writeInsert(self, s:CSharpStringWriter):
        return s
    
    def writeInsertCollection(self, s:CSharpStringWriter):
        return s
    
    def writeUpdate(self, s:CSharpStringWriter):
        return s
    
    def writeDelete(self, s:CSharpStringWriter):
        return s
    
    def writeSelectSingleRecordByPK(self, s:CSharpStringWriter):
        return s
    
    def writeSelectWhere(self, s:CSharpStringWriter):
        return s

    def writeDLClassClose(self, s:CSharpStringWriter):
        s.c()
        return s