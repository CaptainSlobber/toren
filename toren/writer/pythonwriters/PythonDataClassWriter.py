import collections
import json
import os
from pathlib import Path

from typing import List
from ..WriterObject import WriterObject
from ..PropertyWriter import PropertyWriter
from ..StringWriter import StringWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class PythonDataClassWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.StringWriterClass = StringWriter
        self.Class = class_
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)
