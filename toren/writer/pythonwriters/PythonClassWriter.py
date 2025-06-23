import collections
import json
import os
from pathlib import Path

from typing import List
from .PythonPropertyWriter import PythonPropertyWriter
from ..WriterObject import WriterObject
from ..ClassWriter import ClassWriter
from ..PropertyWriter import PropertyWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class PythonClassWriter(ClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Class = class_
        self.PropertyWritersClass = PythonPropertyWriter
        self.Language = language
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()