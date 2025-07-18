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
                fkdep = f"from .{property.ForeignKey.FKClass.Name} import {property.ForeignKey.FKClass.Name}"
                dependency_map[fkdep] = fkdep
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
    

    def writeClassCollectionOpen(self, s):
        s.write(f"class {self.Class.Name}{self.SetDescription}:").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" {self.Class.Description} {self.SetDescription}")
        s.wln("\"\"\"")
        s.ret()

        return s
    


    def writeClassCollectionInitializer(self, s:PythonStringWriter):

        s.wln("def __init__(self):").o()
        s.wln("self.Data = collections.OrderedDict()")
        s.c()

        return s


    def writeClassCollectionAddItem(self, s:PythonStringWriter):
        pkcls = self.getPrimaryKeyClass()
        s.wln(f"def appendItem(self, _{self.Class.Name.lower()}: {self.Class.Name}):").o()
        s.wln(f"self.Data[_{self.Class.Name.lower()}.{pkcls.Name}] = _{self.Class.Name.lower()}").c()

        return s
    
    def writeClassCollectionRemoveItem(self, s:PythonStringWriter):
        pkcls = self.getPrimaryKeyClass()
        s.wln(f"def removeItem(self, {pkcls.Name.lower()}):").o()
        s.wln(f"if {pkcls.Name.lower()} in self.Data:").o()
        s.wln(f"del self.Data[{pkcls.Name.lower()}]").c().c()

        return s
    


    
    def writeClassCollectionGetItem(self, s:PythonStringWriter):
        pkcls = self.getPrimaryKeyClass()
        s.wln(f"def getItem(self, {pkcls.Name.lower()}):").o()
        s.wln(f"if {pkcls.Name.lower()} in self.Data:").o()
        s.wln(f"return self.Data[{pkcls.Name.lower()}]").c()
        s.wln("return None").c()

        return s
    
    def writeClassCollectionGetLength(self, s:PythonStringWriter):
        s.wln("def count(self):").o()
        s.wln("return self.length()").c()

        s.wln("def length(self):").o()
        s.wln("return len(self.Data)").c()
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
        cls = f"from .{self.Class.Name} import {self.Class.Name}"
        dependency_map[_collections] = _collections
        dependency_map[_json] = _json
        dependency_map[_uuid] = _uuid
        dependency_map[cls] = cls
        return dependency_map
    

    def writeClassReferenceCollection(self, _class, s: PythonStringWriter):
        s.wln("\"\"\"")
        s.wln(f" property: {_class.Name} Collection")
        s.wln("\"\"\"")

        setName = "Set"


        s.wln(f"def set{_class.Name}{setName}(self, {_class.Name.lower()}{setName}_: {_class.Name}{self.SetDescription}):")
        s.o().wln(f"self._{_class.Name.lower()}{setName} = {_class.Name.lower()}{setName}_")
        s.c()

        s.wln(f"def get{_class.Name}{setName}(self):")
        s.o().wln(f"return self._{_class.Name.lower()}{setName}")
        s.c()


        return s