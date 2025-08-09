import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .ModuleWriter import ModuleWriter
from .DataModuleWriter import DataModuleWriter
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
        self.DataModuleWriterClass = DataModuleWriter
        self.setLogger(logger)

    def write(self):
        self.Logger.Log(f"Writing {self.Language.Name} Project: {self.Project.Name}")

        self.writeProjectDirectory(project=self.Project)
        self.writeModules(project=self.Project)
        self.writeDataLayer(project=self.Project)

    def writeProjectDirectory(self, project:Project):
        self.writeDirectory(self.Language.OutputDirectory, project.Name)
        self.writeDirectory(os.path.join(self.Language.OutputDirectory, project.Name), project.Name)



    def writeDataLayer(self, project: Project):
        for moduleid, module in project.Modules.Data.items():
            for databaseid, database in project.Datastores.Data.items():
                dm = self.DataModuleWriterClass(project=project, module=module, language=self.Language, database=database, logger=self.Logger)
                dm.write()

    def writeModules(self, project:Project):
        for moduleid, module in project.Modules.Data.items():
            m = self.ModuleWriterClass(project=project, module=module, language=self.Language, logger=self.Logger)
            m.write()




