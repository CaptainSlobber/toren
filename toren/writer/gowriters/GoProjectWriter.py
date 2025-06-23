import collections
import json
import os
from pathlib import Path

from typing import List
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class GoProjectWriter():

    def __init__(self, project: Project, language: Language, logger:Logger=None):
        self.Project = project
        self.Language = language
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()

    def write(self):
        self.Logger.Log(f"Writing project {self.Project.name}")