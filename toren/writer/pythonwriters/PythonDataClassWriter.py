import collections
import json
import os
from pathlib import Path

from typing import List
from ..DataClassWriter import DataClassWriter
from .PythonStringWriter import PythonStringWriter
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class PythonDataClassWriter(DataClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         database=database,
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.StringWriterClass = PythonStringWriter
        self.Class = class_
        self.Database = database
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)
