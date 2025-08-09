import collections
import json
import os
from pathlib import Path

from typing import List
from ..datastores.Database import Database
from .WriterObject import WriterObject
from .ClassWriter import ClassWriter
from .DataClassWriter import DataClassWriter
from .StringWriter import StringWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class

from ..languages import *
from ..tracer.Logger import Logger

class DataModuleWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.Language = language
        self.Database = database
        self.DataClassWriterClass = DataClassWriter
        self.StringWriterClass = StringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)

    def write(self):
        self.Logger.Log(f"=> Writing Data Module: {self.Module.Name}")
        dbmod = f"{self.Module.Name.lower()}_{self.Database.Name.lower()}"
        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                self.Project.Name, 
                                                dbmod)
        self.writePath(data_module_path)



        headerfn = f"{self.HeaderFileName}.{self.Language.DefaultFileExtension}"
        self.writeModuleHeader(data_module_path, headerfn)
        for classid, _class in self.Module.Classes.Data.items():
            c = self.DataClassWriterClass(project=self.Project,
                          module=self.Module,
                          class_=_class,
                          language=self.Language,
                          database=self.Database,
                          logger=self.Logger)
            c.write()

    def writeModuleHeader(self, path, filename):
        s = self.S
        for classid, _class in self.Module.Classes.Data.items():
            pass
