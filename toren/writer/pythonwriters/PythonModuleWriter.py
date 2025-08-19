import collections
import json
import os
from pathlib import Path

from typing import List
from .PythonClassWriter import PythonClassWriter
from ..WriterObject import WriterObject
from ..ModuleWriter import ModuleWriter
from ..ClassWriter import ClassWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class PythonModuleWriter(ModuleWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Language = language
        self.ClassWriterClass = PythonClassWriter
        self.HeaderFileName = f"__init__"
        self.setLogger(logger)

    def writeModuleHeader(self, path, filename):
        s = self.S
        for classid, _class in self.Module.Classes.Data.items():
            s.wln(f"from .{_class.Name} import {_class.Name}")

        for classid, _class in self.Module.Classes.Data.items():
            s.wln(f"from .{_class.SetDescription} import {_class.SetDescription}")
        self.writeFile(path, filename, s.toString())
        