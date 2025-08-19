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

        for propertyid, property in self.Class.Properties.Data.items():
            if property.ForeignKey is not None:
                if property.ForeignKey.FKClassID == self.Class.ID:
                    fkdep = f"from typing import Self"
                    dependency_map[fkdep] = fkdep
                else:
                    fkdep = f"from .{property.ForeignKey.FKClass.Name} import {property.ForeignKey.FKClass.Name}"
                    dependency_map[fkdep] = fkdep

        for _classid, _class in self.Module.Classes.Data.items():
            for _propertyid, _property in _class.Properties.Data.items():
                if _property.ForeignKey is not None:
                    if _property.ForeignKey.FKClassID == self.Class.ID:
                        coll = f"{_class.SetDescription}"
                        reference_coll_dep = f"from .{coll} import {coll}"
                        dependency_map[reference_coll_dep] = reference_coll_dep
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
                s.wln(f"{property.Name.lower()}: {property.Python_Type()} = {property.Python_DefaultValue()},")
        return s

    def writeClassInitializer(self, s: PythonStringWriter):

        s.wln("def __init__(self,")
        s.o().o()
        s = self.writeParentClassParameters(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"{property.Name.lower()}: {property.Python_Type()} = {property.Python_DefaultValue()},")
        
        s.rem(2).c().wln("):").ret()

        s = self.writeParentClassInitializer(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"self.{property.Name} = {property.Name.lower()}")

        s.c()
        s.ret()
        return s
    

    def writeClassCollectionOpen(self, s):
        s.write(f"class {self.Class.SetDescription}:").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" {self.Class.SetDescription}")
        s.wln("\"\"\"")
        s.ret()

        return s
    


    def writeClassCollectionInitializer(self, s:PythonStringWriter):

        s.wln("def __init__(self):").o()
        s.wln("self.Data = collections.OrderedDict()")
        s.c()

        return s


    def writeClassCollectionAddItem(self, s:PythonStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.wln(f"def appendItem(self, _{self.Class.Name.lower()}):").o()
        #s.wln(f"def appendItem(self, _{self.Class.Name.lower()}: {self.Class.Name}):").o()
        s.wln(f"self.Data[_{self.Class.Name.lower()}.{pkproperty.Name}] = _{self.Class.Name.lower()}").c()

        return s
    
    def writeClassCollectionRemoveItem(self, s:PythonStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.wln(f"def removeItem(self, {pkproperty.Name.lower()}):").o()
        s.wln(f"if {pkproperty.Name.lower()} in self.Data:").o()
        s.wln(f"del self.Data[{pkproperty.Name.lower()}]").c().c()
        return s
    
    def writeClassCollectionGetItem(self, s:PythonStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.wln(f"def getItem(self, {pkproperty.Name.lower()}):").o()
        s.wln(f"if {pkproperty.Name.lower()} in self.Data:").o()
        s.wln(f"return self.Data[{pkproperty.Name.lower()}]").c()
        s.wln("return None").c()
        return s
    
    def writeClassCollectionGetLength(self, s:PythonStringWriter):
        s.wln("def count(self):").o()
        s.wln("return self.length()").c()

        s.wln("def length(self):").o()
        s.wln("return len(self.Data)").c()
        return s
    
    def writeClassCollectionFromList(self, s:PythonStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.wln(f"def fromList(self, {self.Class.Name}List):").o()
        #s.wln(f"self.Data = collections.OrderedDict({self.Class.Name}List)")
        s.wln(f"self.Data = collections.OrderedDict()")
        s.wln(f"for _{self.Class.Name.lower()} in {self.Class.Name}List:").o()
        s.wln(f"self.Data[_{self.Class.Name.lower()}.{pkproperty.Name}] = _{self.Class.Name.lower()}").c()
        s.wln("return self").c()
        return s

    def writeClassCollectionToList(self, s:PythonStringWriter):
        s.wln(f"def toList(self):").o()
        s.wln(f"return list(self.Data.values())").c()
        return s 
    
    def writeClassCollectionToDictionary(self, s:PythonStringWriter):
        s.wln(f"def toDict(self):").o()
        s.wln(f"return dict(self.Data)").c()
        return s

    def writeClassCollectionFromDictionary(self, s:PythonStringWriter):
        s.wln(f"def fromDict(self, {self.Class.Name}Dict: dict = {{}}):").o()
        s.wln(f"self.Data = collections.OrderedDict(sorted({self.Class.Name}Dict.items()))")
        s.wln("return self").c()
        return s 
    
    def writeClassCollectionClose(self, s:PythonStringWriter):
        s.c()
        return s  

    def getClassCollectionDependencies(self):
        dependency_map = {}
        _collections = "import collections" 


        _typing = "from typing import List"
        _json = "import json"
        _uuid = "import uuid"
        #cls = f"from .{self.Class.Name} import {self.Class.Name}"
        dependency_map[_collections] = _collections
        dependency_map[_json] = _json
        dependency_map[_uuid] = _uuid
        #dependency_map[cls] = cls
        return dependency_map
    

    def writeClassReferenceCollection(self, _class, s: PythonStringWriter):
        s.wln("\"\"\"")
        s.wln(f" property: {_class.PluralName} ({_class.Name} Collection)")
        s.wln("\"\"\"")

        s.wln(f"def set{_class.PluralName}(self, {_class.PluralName.lower()}_: {_class.SetDescription}):")
        s.o().wln(f"self._{_class.PluralName.lower()} = {_class.PluralName.lower()}_")
        s.c()

        s.wln(f"def get{_class.PluralName}(self):")
        s.o().wln(f"return self._{_class.PluralName.lower()}")
        s.c()


        return s