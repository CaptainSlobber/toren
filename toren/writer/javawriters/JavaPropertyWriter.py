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

class JavaPropertyWriter(PropertyWriter):

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
        s.wln(f" type: {self.Property.Java_Type()} = {self.Property.Type}")
        s.wln(f" description: {self.Property.Description}")
        s.wln("*/")

        # TODO: use uuid for property ID
        s.w(f"public String get{self.Property.Name}PID() ").o()
        s.wln(f'return "{self.Property.ID}";')
        s.c().ret()


        s.wln(f"private {self.Property.Java_Type()} _{self.Property.Name.lower()} = {self.Property.Java_DefaultValue()};").ret()
        s.w(f"public {self.Property.Java_Type()} get{self.Property.Name}() ").o()
        s.wln(f"return this._{self.Property.Name.lower()};")
        s.c().ret()
        s.w(f"public void set{self.Property.Name}({self.Property.Java_Type()} value) ").o()
        s.wln(f"this._{self.Property.Name.lower()} = value;")
        s.c().ret()

        if self.Property.ForeignKey is not None:
            s = self.writeForeignKeyProperty(s)

        return s
    

    def writeForeignKeyProperty(self, s):

        fktype = self.Property.ForeignKey.FKClass.Name
        s.wln(f"private {fktype} _{self.Property.ForeignKey.PropertyName.lower()};").ret()
        s.w(f"public {fktype} get{self.Property.ForeignKey.PropertyName}() ").o()
        s.wln(f"return this._{self.Property.ForeignKey.PropertyName.lower()};")
        s.c().ret()
        s.w(f"public void set{self.Property.ForeignKey.PropertyName}({fktype} value) ").o()
        s.wln(f"this._{self.Property.ForeignKey.PropertyName.lower()} = value;")
        s.c().ret()

        return s

