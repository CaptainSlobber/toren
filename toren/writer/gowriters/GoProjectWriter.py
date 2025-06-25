import collections
import json
import os
from pathlib import Path

from typing import List
from ..ModuleWriter import ModuleWriter
from ..ProjectWriter import ProjectWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class GoProjectWriter(ProjectWriter):

    def __init__(self, project: Project, language: Language, logger:Logger=None):
        super().__init__(project=project, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Language = language
        self.ModuleWriterClass = ModuleWriter
        self.setLogger(logger)