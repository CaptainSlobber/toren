import collections
import json
import os
from pathlib import Path

from typing import List

from numpy import mod
from .CSharpClassWriter import CSharpClassWriter
from .CSharpStringWriter import CSharpStringWriter
from ...datastores.Database import Database     
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
        self.DeleteOutputDirectory = deleteoutputdirectory
        self.Project = project
        self.Module = module
        self.Language = language
        self.ClassWriterClass = CSharpClassWriter
        self.StringWriterClass = CSharpStringWriter
        self.HeaderFileName = f"{self.Module.Name}"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)

    def writeModuleHeader(self, path, filename):
        s = self.S
        pass

    def getModulePath(self):
        
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        t = self.Module.ParentProject.TLD.lower()

        mod = f"{e.lower()}.{p.lower()}.{self.Module.Name.lower()}"
        module_path = os.path.join(self.Language.OutputDirectory, p, mod)

        self.writeDirectory(module_path, False)
        return module_path