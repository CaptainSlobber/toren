import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .ClassWriter import ClassWriter
from .StringWriter import StringWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class ModuleWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.Language = language
        self.ClassWriterClass = ClassWriter
        self.StringWriterClass = StringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)
        
    def write(self):
        self.Logger.Log(f"=> Writing Module: {self.Module.Name}")
        parent_project_path = self.getParentProjectPath(self.Language, self.Project)
        module_path = self.writeDirectory(parent_project_path, self.Module.Name)
        headerfn = f"{self.HeaderFileName}.{self.Language.DefaultFileExtension}"
        self.writeModuleHeader(module_path, headerfn)
        for classid, _class in self.Module.Classes.Data.items():
            c = self.ClassWriterClass(project=self.Project,
                          module=self.Module,
                          class_=_class,
                          language=self.Language,
                          logger=self.Logger)
            c.write()

    def writeModuleHeader(self, path, filename):
        s = self.S
        for classid, _class in self.Module.Classes.Data.items():
            pass

            
            
