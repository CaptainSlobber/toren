import collections
import json
import os
from pathlib import Path

from typing import List
from .CSharpClassWriter import CSharpClassWriter
from ..ModuleWriter import ModuleWriter
from ...Project import Project
from ...Module import Module
from ...languages import *
from ...tracer.Logger import Logger

class CSharpModuleWriter(ModuleWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 logger:Logger=None, 
                 deleteoutputdirectory:bool=False):
        super().__init__(project=project, 
                         module=module, 
                         language=language, 
                         logger=logger,
                         deleteoutputdirectory=deleteoutputdirectory)
        self.Project = project
        self.Module = module
        self.Language = language
        self.DeleteOutputDirectory = deleteoutputdirectory
        self.ClassWriterClass = CSharpClassWriter
        self.HeaderFileName = f""
        self.setLogger(logger)

    def writeModuleHeader(self, path, filename):
        s = self.S
        pass