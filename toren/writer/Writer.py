import collections
import json
import os
from pathlib import Path

from typing import List
from ..Project import Project
from ..Module import Module
from ..languages import *
from ..tracer.Logger import Logger

class Writer():

    def __init__(self, project):
        self.Project = project
        self.Logger = Logger()

    def write(self):
        n =  self.Project.Name 
        v = str(self.Project.Version)
        self.Logger.Log(f"Writing Project: {n} ({v})")
        self.writeProjectDirectory(project=self.Project)
        self.writeModules(project=self.Project)

    def writeProjectDirectory(self, project:Project):
        for languageid, language in project.Languages.Data.items():
            self.writeDirectory(language.OutputDirectory, project.Name, False)
            self.writeDirectory(os.path.join(language.OutputDirectory, project.Name), project.Name, True)

    def writeDirectory(self, path, dirname, writeinit=False):
        directory = os.path.join(path, dirname)
        if not os.path.exists(directory):
            os.makedirs(directory)


    def writeModules(self, project:Project):
        for languageid, language in project.Languages.Data.items():
            for moduleid, module in project.Modules.Data.items():
                self.writeModule(module=module, language=language)
    

    def getParentProjectPath(self, language: Language):
        return os.path.join(language.OutputDirectory, self.Project.Name, self.Project.Name)

    def writeModule(self, module: Module, language: Language):
        self.Logger.Log(f"Writing Module: {module.Name}")
        self.writeDirectory(self.getParentProjectPath(language), module.Name, True)

            


        
