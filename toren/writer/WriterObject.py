import collections
import json
import os
from pathlib import Path

from typing import List
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class WriterObject():

    def __init__(self):
        #self.Logger = Logger()
        pass


    def writeDirectory(self, path, dirname):
        directory = os.path.join(path, dirname)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def createFile(self, path, filename):
        return self.writeFile(path, filename, "")

    def writeFile(self, path, filename, content):
        file_path = os.path.join(path, filename)
        with open(file_path, "w") as file:
            file.write(content)
        return file_path



    def getParentProjectPath(self, language: Language, project: Project):
        return os.path.join(language.OutputDirectory, project.Name, project.Name)
    

    def getParentModulePath(self, language: Language, project: Project, module: Module):
        return os.path.join(language.OutputDirectory, project.Name, project.Name,  module.Name)