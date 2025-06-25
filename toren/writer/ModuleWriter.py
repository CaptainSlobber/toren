import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .ClassWriter import ClassWriter
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
        self.setLogger(logger)
        
    def setLogger(self, logger: Logger):
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()
        return self.Logger

    def write(self):
        self.Logger.Log(f"=> Writing Module: {self.Module.Name}")
        parent_project_path = self.getParentProjectPath(self.Language, self.Project)
        self.writeDirectory(parent_project_path, self.Module.Name)
        for classid, _class in self.Module.Classes.Data.items():
            c = self.ClassWriterClass(project=self.Project,
                          module=self.Module,
                          class_=_class,
                          language=self.Language,
                          logger=self.Logger)
            c.write()

            
