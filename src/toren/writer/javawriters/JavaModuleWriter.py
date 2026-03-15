import collections
import json
import os
from pathlib import Path

from typing import List
from .JavaClassWriter import JavaClassWriter
from ..ModuleWriter import ModuleWriter
from ...Project import Project
from ...Module import Module
from ...languages import *
from ...tracer.Logger import Logger

class JavaModuleWriter(ModuleWriter):

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
        self.ClassWriterClass = JavaClassWriter
        self.HeaderFileName = f""
        self.setLogger(logger)

    def writeModuleHeader(self, path, filename):
        s = self.S
        pass

    

    def getModulePath(self):
        
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        t = self.Module.ParentProject.TLD.lower()
        src = "src"
        main = "main"
        java = "java"

        module_path = os.path.join(self.Language.OutputDirectory, p, m, src, main, java, t, e, p, m)

        self.writeDirectory(module_path, True)
        return module_path