import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .ModuleWriter import ModuleWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class ProjectWriter(WriterObject):

    def __init__(self, project: Project, language: Language, logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Language = language
        self.ModuleWriterClass = ModuleWriter
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()

    def write(self):
        self.Logger.Log(f"Writing {self.Language.Name} Project: {self.Project.Name}")

        self.writeProjectDirectory(project=self.Project)
        self.writeModules(project=self.Project)

    def writeProjectDirectory(self, project:Project):
        self.writeDirectory(self.Language.OutputDirectory, project.Name)
        self.writeDirectory(os.path.join(self.Language.OutputDirectory, project.Name), project.Name)



    def writeModules(self, project:Project):
        for moduleid, module in project.Modules.Data.items():
            m = self.ModuleWriterClass(project=project, module=module, language=self.Language, logger=self.Logger)
            m.write()




