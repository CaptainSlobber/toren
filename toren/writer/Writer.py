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
from .WriterObject import WriterObject
from .ProjectWriter import ProjectWriter
from .pythonwriters.PythonProjectWriter import PythonProjectWriter
from .csharpwriters.CSharpProjectWriter import CSharpProjectWriter
from .javascriptwriters.JavaScriptProjectWriter import JavaScriptProjectWriter
from .javawriters.JavaProjectWriter import JavaProjectWriter
from .gowriters.GoProjectWriter import GoProjectWriter

class Writer(WriterObject):

    def __init__(self, project):
        super().__init__()
        self.Project = project
        self.Logger = Logger()

    def write(self):
        n =  self.Project.Name 
        v = str(self.Project.Version)
        self.Logger.Log(f"Writing Project: {n} ({v})")
        for languageid, language in self.Project.Languages.Data.items():
            if language.ID == LanguagePython().getID():
                w = PythonProjectWriter(project=self.Project, language=language, logger=self.Logger)
                w.write()
            elif language.ID == LanguageCSharp().getID():
                w = CSharpProjectWriter(roject=self.Project, language=language, logger=self.Logger)
                w.write()
            elif language.ID == LanguageJavaScript().getID():
                w = JavaScriptProjectWriter(roject=self.Project, language=language, logger=self.Logger)
                w.write()
            elif language.ID == LanguageJava().getID():
                w = JavaProjectWriter(roject=self.Project, language=language, logger=self.Logger)
                w.write()
            elif language.ID == LanguageGo().getID():
                w = GoProjectWriter(roject=self.Project, language=language, logger=self.Logger)
                w.write()
            else:
                w = ProjectWriter(project=self.Project, language=language, logger=self.Logger)
                w.write()




            


        
