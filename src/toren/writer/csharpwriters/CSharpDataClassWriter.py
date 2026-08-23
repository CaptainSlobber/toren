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
        self.StringWriterClass = CSharpStringWriter
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
        for dependency in self.Database.CSharpDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        

        return dependency_map
    

    def getDataModulePath(self) -> str:
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        t = self.Module.ParentProject.TLD.lower()

        dbmod = f"{e.lower()}.{p.lower()}.{self.Module.Name.lower()}.{self.Database.Name.lower()}"
        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                dbmod)
        return data_module_path

    def writeDLClassOpen(self, s:CSharpStringWriter):

        
        c = self.Class.Name
        d = self.getDLClassName()
        
        s.ret()
        s.write(f"public static class {d} ").o()
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
        #d = self.getDLClassName()
        #s.wln(f"public {d}() {{}}")
        #s.ret()
        return s

    def writeDLClassClose(self, s:CSharpStringWriter):
        s.c()
        return s