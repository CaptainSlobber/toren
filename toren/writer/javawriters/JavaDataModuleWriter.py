import collections
import json
import os
from pathlib import Path

from typing import List
from ...datastores.Database import Database
from ..DataModuleWriter import DataModuleWriter
from .JavaClassWriter import JavaClassWriter
from .JavaDataClassWriter import JavaDataClassWriter
from .JavaStringWriter import JavaStringWriter
from ...Project import Project
from ...Module import Module

from ...languages import *
from ...tracer.Logger import Logger

class JavaDataModuleWriter(DataModuleWriter):

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
        self.ClassWriterClass = JavaClassWriter
        self.DataClassWriterClass = JavaDataClassWriter
        self.StringWriterClass = JavaStringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def writeCommonDataFunctions(self, path, classname):
        s = self.S
        s.clear()
        s.write(f"public static class {classname} ").o()

        s.wln("/*")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Datalayer Functions")
        s.wln("*/")
        s.ret()

        s.c()
        s.ret()
        
        filename = f"{classname}.{self.Language.DefaultFileExtension}"
        self.writeFile(path, filename, s.toString())