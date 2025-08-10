import collections
import json
import os
from pathlib import Path

from typing import List
from ..StringWriter import StringWriter
from ..PropertyWriter import PropertyWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...datatypes import *
from ...tracer.Logger import Logger

class CSharpPropertyWriter(PropertyWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 property: Datatype,
                 language: Language, 
                 stringWriter: StringWriter = None,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         property=property, 
                         language=language, 
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Class = class_
        self.Property = property
        self.Language = language
        self.S = stringWriter
        self.setLogger(logger)


    def write(self):
        self.Logger.Log(f"   - Writing {self.Language.Name} Property: {self.Property.Name} [{self.Property.Type}]")
        s = self.S
        
        s.wln("/*")
        s.wln(f" property: {self.Property.Name}")
        s.wln(f" type: {self.Property.CSharp()} = {self.Property.Type}")
        s.wln(f" description: {self.Property.Description}")
        s.wln("*/")

        # TODO: use uuid for property ID
        s.w(f"public string get{self.Property.Name}PID() ").o()
        s.wln(f'return "{self.Property.ID}";')
        s.c()
        s.wln(f"private {self.Property.CSharp()} _{self.Property.Name.lower()};")
        s.w(f"public {self.Property.CSharp()} {self.Property.Name} ").o()
        s.wln(f"get {{ return this._{self.Property.Name.lower()}; }}")
        s.wln(f"set {{ this._{self.Property.Name.lower()} = value; }}")
        s.c().ret()

        if self.Property.ForeignKey is not None:
            
            s = self.writeForeignKeyProperty(s)
        
        
        return s
    

    def writeForeignKeyProperty(self, s):

        fktype = self.Property.ForeignKey.FKClass.Name
        s.wln(f"private {fktype} _{self.Property.ForeignKey.PropertyName.lower()};")
        s.w(f"public {fktype} {self.Property.ForeignKey.PropertyName} ").o()
        s.wln(f"get {{ return this._{self.Property.ForeignKey.PropertyName.lower()}; }}")
        s.wln(f"set {{ this._{self.Property.ForeignKey.PropertyName.lower()} = value; }}")
        s.c().ret()

        return s

