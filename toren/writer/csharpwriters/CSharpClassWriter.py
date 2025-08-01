import collections
import json
import os
from pathlib import Path

from typing import List
from .CSharpPropertyWriter import CSharpPropertyWriter
from .CSharpStringWriter import CSharpStringWriter
from ..WriterObject import WriterObject
from ..ClassWriter import ClassWriter
from ..PropertyWriter import PropertyWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class CSharpClassWriter(ClassWriter):

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
        self.StringWriterClass = CSharpStringWriter
        self.Class = class_
        self.PropertyWritersClass = CSharpPropertyWriter
        self.Language = language
        self.setLogger(logger)



    def getDependencies(self):
        dependency_map = {}
        for propertyid, property in self.Class.Properties.Data.items():
            for dependency in property.CSharp_Dependencies():
                if dependency not in dependency_map:
                    dependency_map[dependency] = dependency

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                for dependency in property.CSharp_Dependencies():
                    if dependency not in dependency_map:
                        dependency_map[dependency] = dependency

        for propertyid, property in self.Class.Properties.Data.items():
            if property.ForeignKey is not None:
                if property.ForeignKey.FKClassID == self.Class.ID:
                    pass
                else:
                    _clss = property.ForeignKey.FKClass.Name
                    _modl = property.ForeignKey.FKClass.ParentModule.Name
                    _proj = property.ForeignKey.FKClass.ParentModule.ParentProject.Name
                    fkdep = f"using {_proj}.{_modl}.{_clss};"
                    dependency_map[fkdep] = fkdep

        for _classid, _class in self.Module.Classes.Data.items():
            for _propertyid, _property in _class.Properties.Data.items():
                if _property.ForeignKey is not None:
                    if _property.ForeignKey.FKClassID == self.Class.ID:
                        _modl = _class.ParentModule.Name
                        _proj = _class.ParentModule.ParentProject.Name
                        coll = f"{_class.Name}{self.SetDescription}"
                        reference_coll_dep = f"using {_proj}.{_modl}.{coll};"
                        dependency_map[reference_coll_dep] = reference_coll_dep
        return dependency_map

    
    def writeClassOpen(self, s: CSharpStringWriter):
        if self.Class.InheritsFrom is not None:
            pproj = self.Class.InheritsFrom.ParentModule.ParentProject.Name
            pmodl = self.Class.InheritsFrom.ParentModule.Name
            pclss = self.Class.InheritsFrom.Name
            s.wln(f"using {pproj}.{pmodl}.{pclss};")
            s.ret()
            s.write(f"public class {self.Class.Name}: {self.ParentClassName} ").o()
        else:
            s.write(f"public class {self.Class.Name} ").o()
        
        s.ret()
        s.wln("/*")
        s.wln(f" Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln(f" Description {self.Class.Description}")
        s.wln("*/")
        s.ret()
        return s
    

    def writeParentClassInitializer(self, s:CSharpStringWriter):
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f"this._{property.Name} = {property.Name.lower()};")

        return s


    def writeParentClassParameters(self, s:CSharpStringWriter):
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f"{property.CSharp()} {property.Name.lower()} = {property.CSharp_DefaultValue()},")
        return s

    def writeClassInitializer(self, s: CSharpStringWriter):
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        s.wln(f"public {self.Class.Name} (").Inc(2)

        s = self.writeParentClassParameters(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"{property.CSharp()} {property.Name.lower()} = {property.CSharp_DefaultValue()},")
        
        
        s.rem(2).newline()
        s.Dec()
        s.a(")").o()
        s.Dec()
        s.ret()
        s = self.writeParentClassInitializer(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"this._{property.Name} = {property.Name.lower()};")
        s.ret()
        s.c()
        s.ret()
        return s
    

    def writeClassReferenceCollection(self, _class, s: CSharpStringWriter):
        s.wln("/*")
        s.wln(f" property: {_class.Name} Collection")
        s.wln("*/")

        setName = "Set" # TODO: Parameterize 


        s.wln(f"private {_class.Name}{self.SetDescription} _{_class.Name.lower()}{setName};").ret()
        s.w(f"public {_class.Name}{self.SetDescription} {_class.Name}{setName} ").o()
        s.wln(f"get {{ return this._{_class.Name.lower()}{setName}; }}")
        s.wln(f"set {{ this._{_class.Name.lower()}{setName} = value; }}")
        s.c().ret()


        return s