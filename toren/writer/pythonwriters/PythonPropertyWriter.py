import collections
import json
import os
from pathlib import Path

from typing import List
from ..WriterObject import WriterObject
from ..PropertyWriter import PropertyWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...datatypes import *
from ...tracer.Logger import Logger

class PythonPropertyWriter(PropertyWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 property: Datatype,
                 language: Language, 
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         property=property, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Class = class_
        self.Property = property
        self.Language = language
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()

    def write(self):
        self.Logger.Log(f"   - Writing {self.Language.Name} Property: {self.Property.Name} [{self.Property.Type}]")