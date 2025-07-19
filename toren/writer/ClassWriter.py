import collections
import json
import os
from pathlib import Path

from typing import List
from .WriterObject import WriterObject
from .PropertyWriter import PropertyWriter
from .StringWriter import StringWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger

class ClassWriter(WriterObject):

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
        self.PropertyWritersClass = PropertyWriter
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.SetDescription = self.getSetDescription()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)


    def setLogger(self, logger: Logger):
        if logger is not None:
            self.Logger = logger
        else:
            self.Logger = Logger()
        return self.Logger
    
    '''
        Class
    '''
    
    def getParentClassName(self):
        if self.Class.InheritsFrom is not None:
            return self.Class.InheritsFrom.Name
        return ""

    def getDependencies(self):
        dependency_map = {}
        for propertyid, property in self.Class.Properties.Data.items():
            pass
        return dependency_map


    def writeDependencies(self, dependency_map, s:StringWriter):
        
        for dependencyid, dependency in dependency_map.items():
            s.wln(f"{dependency}")
        
        s.ret()
        return s
    
    def writeClassOpen(self, s:StringWriter):
        s.write(f"class {self.Class.Name}").o()
        s.wln(f" ")
        s.wln(f"// {self.Class.Description}")
        s.wln(f" ")
        return s
    
    def writeParentClassInitializer(self, s:StringWriter):
        return s

    def writeClassInitializer(self, s:StringWriter):

        s.wln("init() {}")
        return s
    
    def writeClassProperties(self, s:StringWriter):
        for propertyid, property in self.Class.Properties.Data.items():
            c = self.PropertyWritersClass(project=self.Project,
                          module=self.Module,
                          class_=self.Class,
                          property=property,
                          language=self.Language,
                          stringWriter=self.S,
                          logger=self.Logger)
            c.write()
        return s
    

    def writeClassClose(self, s:StringWriter):
        s.c()
        return s
    

    def createClassFile(self, s:StringWriter):
        module_path = self.getParentModulePath(self.Language, self.Project, self.Module)
        fn = f"{self.Class.Name}.{self.Language.DefaultFileExtension}"
        self.writeFile(module_path, fn, s.toString())

    def write(self):
        self.writeClass()
        self.writeClassCollection()

    def writeClassReferenceCollections(self, s:StringWriter):
        s.ret()

        for _classid, _class in self.Module.Classes.Data.items():
            for _propertyid, _property in _class.Properties.Data.items():
                if _property.ForeignKey is not None:
                    if _property.ForeignKey.FKClassID == self.Class.ID:
                        s = self.writeClassReferenceCollection(_class, s)
                


        return s

    def writeClassReferenceCollection(self, _class, s:StringWriter):
        return s


    def writeClass(self):
        self.Logger.Log(f"  -> Writing {self.Language.Name} Class: {self.Class.Name}")
        self.S = self.StringWriterClass(self.Language)
        s = self.S
        dependencies = self.getDependencies()
        s = self.writeDependencies(dependencies, s)
        s = self.writeClassOpen(s)
        s = self.writeClassInitializer(s)
        s = self.writeClassProperties(s)
        s = self.writeClassReferenceCollections(s)
        s = self.writeClassClose(s)
        self.createClassFile(s)

    '''
        Class Collection
    '''

    def writeClassCollection(self):
        self.Logger.Log(f"  -> Writing {self.Language.Name} Class Collection: {self.Class.Name}")
        self.S = self.StringWriterClass(self.Language)
        s = self.S
        dependencies = self.getClassCollectionDependencies()
        s = self.writeDependencies(dependencies, s)
        s = self.writeClassCollectionOpen(s)
        s = self.writeClassCollectionInitializer(s)
        s = self.writeClassCollectionProperties(s)
        s = self.writeClassCollectionClose(s)
        self.createClassCollectionFile(s)


    def writeClassCollectionOpen(self, s):
        s.write(f"class {self.Class.Name}{self.SetDescription}").write(" {").o()
        s.wln(f" ")
        s.wln(f"// {self.Class.Description}")
        s.wln(f" ")
        return s
    


    def writeClassCollectionInitializer(self, s:StringWriter):

        s.wln("init() {}")
        return s
    
    def writeClassCollectionProperties(self, s:StringWriter):
        s = self.writeClassCollectionAddItem(s)
        s = self.writeClassCollectionRemoveItem(s)
        s = self.writeClassCollectionGetItem(s)
        s = self.writeClassCollectionGetLength(s)
        return s
    
    def getPrimaryKeyClass(self):
        for propertyid, property in self.Class.Properties.Data.items():
            if property.IsPrimaryKey:
                return property
        for propertyid, property in self.Class.InheritedProperties.Data.items():
            if property.IsPrimaryKey:
                return property
    

    def writeClassCollectionAddItem(self, s:StringWriter):
        return s
    
    def writeClassCollectionRemoveItem(self, s:StringWriter):
        return s
    
    def writeClassCollectionGetItem(self, s:StringWriter):
        return s
    
    def writeClassCollectionGetLength(self, s:StringWriter):
        return s
    
    def writeClassCollectionClose(self, s:StringWriter):
        s.c()
        s.wln("}")
        return s  

    def getClassCollectionDependencies(self):
        dependency_map = {}
        return dependency_map

    def getSetDescription(self):

        # Collection, Array, Set etc
        return "Collection"
    

    def createClassCollectionFile(self, s:StringWriter):
        module_path = self.getParentModulePath(self.Language, self.Project, self.Module)
        fn = f"{self.Class.Name}{self.SetDescription}.{self.Language.DefaultFileExtension}"
        self.writeFile(module_path, fn, s.toString())