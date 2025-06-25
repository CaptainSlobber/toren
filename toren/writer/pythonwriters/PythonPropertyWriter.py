import collections
import json
import os
from pathlib import Path

from typing import List
from ..StringWriter import StringWriter
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
                 stringWriter: StringWriter = None,
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
        self.S = stringWriter
        self.setLogger(logger)

    def write(self):
        self.Logger.Log(f"   - Writing Property: {self.Property.Name} [{self.Property.Type}]")
        s = self.S
        s.wln(f"// property {self.Property.Name} : {self.Property.Type}")
        s.wln(f"property {self.Property.Name} : {self.Property.Type}")
        s.ret()
        return s