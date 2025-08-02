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
        s.wln(f" property: {_class.PluralName} ({_class.Name} Collection)")
        s.wln("*/")

        s.wln(f"private {_class.Name}{self.SetDescription} _{_class.PluralName.lower()};").ret()
        s.w(f"public {_class.Name}{self.SetDescription} {_class.PluralName} ").o()
        s.wln(f"get {{ return this._{_class.PluralName.lower()}; }}")
        s.wln(f"set {{ this._{_class.PluralName.lower()} = value; }}")
        s.c().ret()

        return s
    


    def writeClassCollectionOpen(self, s):
        s.write(f"public class {self.Class.Name}{self.SetDescription} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" {self.Class.Description} {self.SetDescription}")
        s.wln("*/")
        s.ret()

        return s
    


    def writeClassCollectionInitializer(self, s:CSharpStringWriter):


        # +------------------+---------+----------+--------+----------+----------+---------+
        # | Collection       | Indexed | Keyed    | Value  | Addition |  Removal | Memory  |
        # |                  | lookup  | lookup   | lookup |          |          |         |
        # +------------------+---------+----------+--------+----------+----------+---------+
        # | SortedList       | O(1)    | O(log n) | O(n)   | O(n)*    | O(n)     | Lesser  |
        # | SortedDictionary | O(n)**  | O(log n) | O(n)   | O(log n) | O(log n) | Greater |
        # +------------------+---------+----------+--------+----------+----------+---------+
        pkcls = self.getPrimaryKeyClass()
        csharpCollectionObject = f"SortedDictionary<{pkcls.CSharp()}, {self.Class.Name}>"

        s.w(f"public {self.Class.Name}{self.SetDescription}() ").o()
        s.wln(f"this._data = new {csharpCollectionObject}();")
        s.c()

        s.wln(f"private {csharpCollectionObject} _data;").ret()
        s.w(f"public {csharpCollectionObject} Data ").o()
        s.wln(f"get {{ return this._data; }}")
        s.wln(f"set {{ this._data = value; }}")
        s.c().ret()


        return s


    def writeClassCollectionAddItem(self, s:CSharpStringWriter):
        pkcls = self.getPrimaryKeyClass()
        s.w(f"public void appendItem({self.Class.Name} _{self.Class.Name.lower()}) ").o()
        s.wln(f"this._data.Add(_{self.Class.Name.lower()}.{pkcls.Name}, _{self.Class.Name.lower()});")
        s.c().ret()
        return s
    
    def writeClassCollectionRemoveItem(self, s:CSharpStringWriter):
        pkcls = self.getPrimaryKeyClass()
        s.w(f"public bool removeItem({pkcls.CSharp()} {pkcls.Name.lower()}) ").o()
        s.wln(f"return this._data.Remove({pkcls.Name.lower()});")
        s.c().ret()

        return s
    


    
    def writeClassCollectionGetItem(self, s:CSharpStringWriter):
        pkcls = self.getPrimaryKeyClass()
        s.w(f"public {self.Class.Name} getItem({pkcls.CSharp()} {pkcls.Name.lower()}) ").o()
        #s.w(f"if (this.Data.ContainsKey({pkcls.Name.lower()})").o()
        s.wln(f"return this.Data[{pkcls.Name.lower()}];")
        #s.c()
        #s.wln("return null;")
        s.c().ret()

        return s
    
    def writeClassCollectionGetLength(self, s:CSharpStringWriter):

        s.w(f"public int count() ").o()
        s.wln(f"return length();")
        s.c().ret()

        s.w(f"public int length() ").o()
        s.wln(f"return this._data.Count;")
        s.c().ret()
        return s
    
    def writeClassCollectionClose(self, s:CSharpStringWriter):
        s.c()
        return s  

    def getClassCollectionDependencies(self):
        dependency_map = {}
        
        _system = "using System;"
        _collections = "using System.Collections.Generic;" 
        proj = self.Class.ParentModule.ParentProject.Name
        modl = self.Class.ParentModule.Name
        clss = self.Class.Name
        _cls = f"using {proj}.{modl}.{clss};"

        dependency_map[_system] = _system
        dependency_map[_collections] = _collections
        dependency_map[_cls] = _cls

        return dependency_map
    
