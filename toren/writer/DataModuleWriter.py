import collections
import json
import os
from pathlib import Path

from typing import List
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
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.Language = language
        self.DataClassWriterClass = DataClassWriter
        self.StringWriterClass = StringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)
        
    def setLogger(self, logger: Logger):
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()
        return self.Logger

    def write(self):
        self.Logger.Log(f"=> Writing Data Module: {self.Module.Name}")
        parent_project_data_path = self.getParentProjectDataPath(self.Language, self.Project)

        data_module_path = self.writeDirectory(parent_project_data_path,  self.Module.Name)



        headerfn = f"{self.HeaderFileName}.{self.Language.DefaultFileExtension}"
        self.writeModuleHeader(data_module_path, headerfn)
        for classid, _class in self.Module.Classes.Data.items():
            c = self.DataClassWriterClass(project=self.Project,
                          module=self.Module,
                          class_=_class,
                          language=self.Language,
                          logger=self.Logger)
            c.write()

    def writeModuleHeader(self, path, filename):
        s = self.S
        for classid, _class in self.Module.Classes.Data.items():
            pass
