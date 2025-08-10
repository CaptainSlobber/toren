import collections
import json
import os
from pathlib import Path

from typing import List
from ...datastores.Database import Database
from ..DataModuleWriter import DataModuleWriter
from .CSharpDataClassWriter import CSharpDataClassWriter
from .CSharpStringWriter import CSharpStringWriter
from ...Project import Project
from ...Module import Module

from ...languages import *
from ...tracer.Logger import Logger

class CSharpDataModuleWriter(DataModuleWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         language=language, 
                         database=database,
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Language = language
        self.Database = database
        self.DataClassWriterClass = CSharpDataClassWriter
        self.StringWriterClass = CSharpStringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)