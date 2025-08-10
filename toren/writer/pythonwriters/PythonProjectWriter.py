import collections
import json
import os
from pathlib import Path

from typing import List
from .PythonModuleWriter import PythonModuleWriter
from .PythonDataModuleWriter import PythonDataModuleWriter
from ..ProjectWriter import ProjectWriter
from ...Project import Project
from ...languages import *
from ...tracer.Logger import Logger

class PythonProjectWriter(ProjectWriter):

    def __init__(self, project: Project, language: Language, logger:Logger=None):
        super().__init__(project=project, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Language = language
        self.ModuleWriterClass = PythonModuleWriter
        self.DataModuleWriterClass = PythonDataModuleWriter
        self.setLogger(logger)
