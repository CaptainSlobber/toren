import collections
import json
import os
from pathlib import Path

from typing import List

from ...datastores.Database import Database
from ..DataModuleWriter import DataModuleWriter
from .CSharpClassWriter import CSharpClassWriter
from .CSharpDataClassWriter import CSharpDataClassWriter
from .CSharpStringWriter import CSharpStringWriter
from ...Project import Project
from ...Module import Module

from ...languages import *
from ...tracer.Logger import Logger

class CSharpDataModuleWriter(DataModuleWriter):

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
        self.ClassWriterClass = CSharpClassWriter
        self.DataClassWriterClass = CSharpDataClassWriter
        self.StringWriterClass = CSharpStringWriter
        self.HeaderFileName = f"{self.Module.Name}"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.AdminFunctionsClassName = "Admin"
        self.FilterObjectClassName = "Filter"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def getDataDependencies(self):
        dependency_map = {}
        for dependency in self.Database.CSharpDependencies():
            dependency_map[dependency] = dependency
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            #dependency_map[class_dep] = class_dep
        
        return dependency_map
    
    def writeDLPackage(self, s:CSharpStringWriter):
        p = self.Module.ParentProject.Name
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD
        s.wln(f"namespace {e}.{p}.{m}.{b};")
        s.ret()
        return s
    

    def getDatalayerModuleName(self):
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD.lower()
        dlmodule = f"{e.lower()}.{p.lower()}.{self.Module.Name.lower()}.{self.Database.Name.lower()}"
        return dlmodule
    
    def getDataModulePath(self) -> str:
        dbmod = self.getDatalayerModuleName()

        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                dbmod)

        return data_module_path
    

    def writeDataLayerModuleObjects(self, classes):
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        dbmod = f"{m.lower()}.{b.lower()}"
        mDataLayer = Module().initialize(name=dbmod, 
                               description=dbmod, 
                               id="1095d1dd-3c3b-4005-b6c3-9dd9a025743a",
                               classes=classes)
        mDataLayer.setParentProject(self.Project)

        for classid, _class in mDataLayer.Classes.Data.items():
            c = self.ClassWriterClass(project=self.Project,
                          module=mDataLayer,
                          class_=_class,
                          language=self.Language,
                          logger=self.Logger)
            c.write()
        return mDataLayer
   