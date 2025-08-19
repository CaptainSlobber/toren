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

    def writeCommonDataFunctions(self, path, classname):
        s = self.S
        s.clear()
        s.write(f"class {classname}():").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Datalayer Functions")
        s.wln("\"\"\"")
        s.ret()

        filename = f"{classname}.{self.Language.DefaultFileExtension}"
        self.writeFile(path, filename, s.toString())