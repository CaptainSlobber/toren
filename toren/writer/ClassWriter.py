import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .PropertyWriter import PropertyWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class ClassWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.Class = class_
        self.PropertyWritersClass = PropertyWriter
        self.Language = language
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()


    def write(self):
        self.Logger.Log(f"  -> Writing Class: {self.Class.Name}")
        module_path = self.getParentModulePath(self.Language, self.Project, self.Module)
        self.createFile(module_path, f"{self.Class.Name}.{self.Language.DefaultFileExtension}")
        for propertyid, property in self.Class.Properties.Data.items():
            c = self.PropertyWritersClass(project=self.Project,
                          module=self.Module,
                          class_=self.Class,
                          property=property,
                          language=self.Language,
                          logger=self.Logger)
            c.write()

