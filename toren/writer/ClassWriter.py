import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .PropertyWriter import PropertyWriter
from .StringWriter import StringWriter
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
        self.StringWriterClass = StringWriter
        self.Class = class_
        self.PropertyWritersClass = PropertyWriter
        self.Language = language
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)


    def setLogger(self, logger: Logger):
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()
        return self.Logger

    def write(self):

        self.S = self.StringWriterClass(self.Language)
        s = self.S
        self.Logger.Log(f"  -> Writing Class: {self.Class.Name}")
        module_path = self.getParentModulePath(self.Language, self.Project, self.Module)
        fn = f"{self.Class.Name}.{self.Language.DefaultFileExtension}"
        self.createFile(module_path, fn)
        s.write(f"class {self.Class.Name}").o()
        s.wln(f" ")
        s.wln(f"// {self.Class.Description}")
        s.wln(f" ")
        for propertyid, property in self.Class.Properties.Data.items():
            c = self.PropertyWritersClass(project=self.Project,
                          module=self.Module,
                          class_=self.Class,
                          property=property,
                          language=self.Language,
                          stringWriter=self.S,
                          logger=self.Logger)
            c.write()

        s.c()
        self.writeFile(module_path, fn, s.toString())