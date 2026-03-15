import collections
import json
import os
import shutil
from pathlib import Path

from typing import List
from ..datastores.Database import Database
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class WriterObject():

    def __init__(self):
        #self.Logger = Logger()
        pass

    def setLogger(self, logger: Logger):
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()
        return self.Logger

    def clearDirectory(self, directory):
        try:
            shutil.rmtree(directory)
        except:
            print(f"Unable to remove: {directory}")
              
    def writeDirectory(self, directory, clear=False):
        if clear:
            self.clearDirectory(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory
    
    def writeDirectoryToPath(self, path, dirname, clear=False):
        directory = os.path.join(path, dirname)
        return self.writeDirectory(directory=directory, clear=clear)

    def createFile(self, path, filename):
        return self.writeFile(path, filename, "")

    def writeFile(self, path, filename, content):
        file_path = os.path.join(path, filename)
        with open(file_path, "w") as file:
            file.write(content)
        return file_path

 