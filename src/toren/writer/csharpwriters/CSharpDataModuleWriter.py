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
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.FilterObjectClassName = "Filter"
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