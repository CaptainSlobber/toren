import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
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
                 logger:Logger=None):
        super().__init__()
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
        self.Logger.Log(f"   - Writing Property: {self.Property.Name} [{self.Property.Type}]")

