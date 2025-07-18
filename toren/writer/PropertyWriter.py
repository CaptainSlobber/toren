import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .StringWriter import StringWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..datatypes import *
from ..tracer.Logger import Logger

class PropertyWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 property: Datatype,
                 language: Language,
                 stringWriter: StringWriter = None, 
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.Class = class_
        self.Property = property
        self.Language = language
        self.S = stringWriter
        self.setLogger(logger)

    def setLogger(self, logger: Logger):
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()
        return self.Logger

    def write(self):
        self.Logger.Log(f"   - Writing Property: {self.Property.Name} [{self.Property.Type}]")
        s = self.S
        s.wln(f"// property {self.Property.Name} : {self.Property.Type}")
        s.wln(f"property {self.Property.Name} : {self.Property.Type}")
        s.ret()
        return s