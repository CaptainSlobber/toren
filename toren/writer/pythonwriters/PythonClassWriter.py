import collections
import json
import os
from pathlib import Path

from typing import List
from .PythonPropertyWriter import PythonPropertyWriter
from .PythonStringWriter import PythonStringWriter
from ..WriterObject import WriterObject
from ..ClassWriter import ClassWriter
from ..PropertyWriter import PropertyWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class PythonClassWriter(ClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.StringWriterClass = PythonStringWriter
        self.Class = class_
        self.PropertyWritersClass = PythonPropertyWriter
        self.Language = language
        self.setLogger(logger)



    def getDependencies(self):
        dependency_map = {}
        for propertyid, property in self.Class.Properties.Data.items():
            for dependency in property.Python_Dependencies():
                if dependency not in dependency_map:
                    dependency_map[dependency] = dependency
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                for dependency in property.Python_Dependencies():
                    if dependency not in dependency_map:
                        dependency_map[dependency] = dependency
        return dependency_map


    
    def writeClassOpen(self, s: PythonStringWriter):
        if self.Class.InheritsFrom is not None:
            s.wln(f"from .{self.Class.InheritsFrom.Name} import {self.Class.InheritsFrom.Name}")
            s.ret()

        s.write(f"class {self.Class.Name}({self.ParentClassName}):").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln(f" Description {self.Class.Description}")
        s.wln("\"\"\"")
        s.ret()
        return s
    

    def writeParentClassInitializer(self, s:PythonStringWriter):
        if self.Class.InheritsFrom is not None:
            s.wln(f"super().__init__(").o()
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f"{property.Name.lower()}={property.Name.lower()},")

            s.rem(2).c().wln(")").ret()
        return s


    def writeParentClassParameters(self, s:PythonStringWriter):
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f"{property.Name.lower()}: {property.Python()} = {property.Python_DefaultValue()},")
        return s

    def writeClassInitializer(self, s: PythonStringWriter):

        s.wln("def __init__(self,")
        s.o().o()
        s = self.writeParentClassParameters(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"{property.Name.lower()}: {property.Python()} = {property.Python_DefaultValue()},")
        
        s.rem(2).c().wln("):").ret()

        s = self.writeParentClassInitializer(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"self.{property.Name} = {property.Name.lower()}")

        s.c()
        s.ret()
        return s