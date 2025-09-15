import collections
import json
import os
from pathlib import Path

from typing import List
from .JavaModuleWriter import JavaModuleWriter
from .JavaDataModuleWriter import JavaDataModuleWriter
from ..ProjectWriter import ProjectWriter
from ...Project import Project
from ...languages import *
from ...tracer.Logger import Logger

class JavaProjectWriter(ProjectWriter):

    def __init__(self, project: Project, language: Language, logger:Logger=None):
        super().__init__(project=project, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Language = language
        self.ModuleWriterClass = JavaModuleWriter
        self.DataModuleWriterClass = JavaDataModuleWriter
        self.setLogger(logger)

 