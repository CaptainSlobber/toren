import collections
import json
import os
from pathlib import Path

from typing import List
from .JavaPropertyWriter import JavaPropertyWriter
from .JavaStringWriter import JavaStringWriter
from ..ClassWriter import ClassWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class JavaClassWriter(ClassWriter):

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
        self.StringWriterClass = JavaStringWriter
        self.Class = class_
        self.PropertyWritersClass = JavaPropertyWriter
        self.Language = language
        self.setLogger(logger)



    def getDependencies(self):
        dependency_map = {}
        for propertyid, property in self.Class.Properties.Data.items():
            for dependency in property.Java_Dependencies():
                if dependency not in dependency_map:
                    dependency_map[dependency] = dependency

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                for dependency in property.Java_Dependencies():
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
                    fkdep = f"import {_proj}.{_modl}.{_clss};"
                    #dependency_map[fkdep] = fkdep

        for _classid, _class in self.Module.Classes.Data.items():
            for _propertyid, _property in _class.Properties.Data.items():
                if _property.ForeignKey is not None:
                    if _property.ForeignKey.FKClassID == self.Class.ID:
                        _modl = _class.ParentModule.Name
                        _proj = _class.ParentModule.ParentProject.Name
                        coll = f"{_class.SetDescription}"
                        reference_coll_dep = f"import {_proj}.{_modl}.{coll};"
                        #dependency_map[reference_coll_dep] = reference_coll_dep
        return dependency_map

    def writeNamespace(self, s:JavaStringWriter):
        p = self.Class.ParentModule.ParentProject.Name
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name
        b = self.Module.Name.lower()
        s.wln(f"package {m};")
        s.ret()
        return s
    
    def writeClassOpen(self, s: JavaStringWriter):
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        p = self.Class.ParentModule.ParentProject.Name.lower()
        m = self.Class.ParentModule.Name.lower()
        c = self.Class.Name

        if self.Class.InheritsFrom is not None:
            pent = self.Class.InheritsFrom.ParentModule.ParentProject.Entity.lower()
            pproj = self.Class.InheritsFrom.ParentModule.ParentProject.Name.lower()
            pmodl = self.Class.InheritsFrom.ParentModule.Name.lower()
            pclss = self.Class.InheritsFrom.Name.lower()
            #s.wln(f"import {pent}.{pproj}.{pmodl}.{pclss};")
            #s.ret()
            

            s.write(f"public class {self.Class.Name} extends {self.ParentClassName} ").o()
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
    

    def writeParentClassInitializer_(self, s:JavaStringWriter):
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                #s.wln(f"if ({property.Name.lower()}==null) {{ {property.Name.lower()} = {property.Java_DefaultValue()}; }}")
                s.wln(f"this._{property.Name} = {property.Name.lower()};")

        return s
    
    def writeParentClassInitializer(self, s:JavaStringWriter):
        if self.Class.InheritsFrom is not None:
            s.wln(f"super(").Inc(1)
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f"{property.Name.lower()},")
            s.rem(2).a(");").ret()
            s.Dec(1)
            s.ret()
        return s


    def writeParentClassParameters(self, s:JavaStringWriter):
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritsFrom.Properties.Data.items():
                s.wln(f"{property.Java_Type()} {property.Name.lower()},")
        return s

    def writeClassInitializer(self, s: JavaStringWriter):

        
        s.wln(f"public {self.Class.Name} (").Inc(2)

        s = self.writeParentClassParameters(s)
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"{property.Java_Type()} {property.Name.lower()},")
        
        s.rem(2).newline()
        s.Dec()
        s.a(")").o()
        s.Dec()
        s.ret()
        s = self.writeParentClassInitializer(s)


        for propertyid, property in self.Class.Properties.Data.items():
            #s.wln(f"if ({property.Name.lower()}==null) {{ {property.Name.lower()} = {property.Java_DefaultValue()}; }}")
            s.wln(f"this._{property.Name.lower()} = {property.Name.lower()};")
        s.ret()
        s.c()
        s.ret()
        return s
    
    def writePropertyHelperFunctions(self, property, s:JavaStringWriter):
        s = property.Java_Helper_Functions(s)
        return s
    
    def writeClassReferenceCollection(self, _class, s: JavaStringWriter):
        s.wln("/*")
        s.wln(f" property: {_class.PluralName} ({_class.Name} Collection)")
        s.wln("*/")

        s.wln(f"private {_class.SetDescription} _{_class.PluralName.lower()};").ret()
        s.w(f"public {_class.SetDescription} get{_class.PluralName}() ").o()
        s.wln(f"return this._{_class.PluralName.lower()};")
        s.c().ret()
        s.w(f"public void set{_class.PluralName}({_class.SetDescription} value) ").o()
        s.wln(f"this._{_class.PluralName.lower()} = value;")
        s.c().ret()
        return s
    


    def writeClassCollectionOpen(self, s):
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        p = self.Class.ParentModule.ParentProject.Name.lower()
        m = self.Class.ParentModule.Name.lower()
        c = self.Class.Name

        s.write(f"public class {self.Class.SetDescription} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" {self.Class.Description} {self.Class.SetDescription}")
        s.wln("*/")
        s.ret()

        return s
    


    def writeClassCollectionInitializer(self, s:JavaStringWriter):



        JavaCollectionObject = self.getCollectionObject()

        s.w(f"public {self.Class.SetDescription}() ").o()
        #s.wln(f"this._data = new {JavaCollectionObject}();")
        s.wln(f"this._data = new TreeMap<>();")
        s.c()
        s.wln(f"private {JavaCollectionObject} _data;").ret()
        s.w(f"public {JavaCollectionObject} getData() ").o()
        s.wln(f"return this._data;")
        s.c().ret()
        s.w(f"public void setData({JavaCollectionObject} value) ").o()
        s.wln(f"this._data = value;")
        s.c().ret()


        return s
    

    def getCollectionObject(self, collectionType="SortedMap"):
        pkproperty = self.getPrimaryKeyProperty()
        JavaCollectionObject = f"{collectionType}<{pkproperty.Java_Type()}, {self.Class.Name}>"
        return JavaCollectionObject



    def writeClassCollectionAddItem(self, s:JavaStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.w(f"public {self.Class.SetDescription} appendItem({self.Class.Name} _{self.Class.Name.lower()}) ").o()
        s.wln(f"this._data.put(_{self.Class.Name.lower()}.get{pkproperty.Name}(), _{self.Class.Name.lower()});")
        s.wln("return this;")
        s.c().ret()
        return s
    
    def writeClassCollectionRemoveItem(self, s:JavaStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.w(f"public void removeItem({pkproperty.Java_Type()} {pkproperty.Name.lower()}) ").o()
        s.wln(f"this._data.remove({pkproperty.Name.lower()});")
        s.c().ret()
        return s
    
    def writeClassCollectionGetItem(self, s:JavaStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        s.w(f"public {self.Class.Name} getItem({pkproperty.Java_Type()} {pkproperty.Name.lower()}) ").o()
        s.wln(f"return this._data.get({pkproperty.Name.lower()});")
        s.c().ret()

        return s
    
    def writeClassCollectionGetLength(self, s:JavaStringWriter):

        s.w(f"public int count() ").o()
        s.wln(f"return length();")
        s.c().ret()

        s.w(f"public int length() ").o()
        s.wln(f"return this._data.size();")
        s.c().ret()
        return s
    
    def writeClassCollectionFromArray(self, s:JavaStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        JavaCollectionObject = self.getCollectionObject()
        s.w(f"public {self.Class.SetDescription} fromArray({self.Class.Name}[] {self.Class.Name.lower()}Arr)" ).o()
        #s.wln(f"this._data = new {JavaCollectionObject}();")
        s.wln(f"this._data = new TreeMap<>();")
        s.w(f"for (int i = 0; i < {self.Class.Name.lower()}Arr.length; i++)").o()
        s.wln(f"this._data.put({self.Class.Name.lower()}Arr[i].get{pkproperty.Name}(), {self.Class.Name.lower()}Arr[i]);").c()
        s.wln("return this;").c().ret()
        return s

    def writeClassCollectionToArray(self, s:JavaStringWriter):
        s.w(f"public {self.Class.Name}[] toArray()" ).o()
        s.wln(f"{self.Class.Name}[] arr = ({self.Class.Name}[]) this._data.values().toArray();")
        s.wln("return arr;").c().ret()
        return s 

    def writeClassCollectionFromList(self, s:JavaStringWriter):
        pkproperty = self.getPrimaryKeyProperty()
        JavaCollectionObject = self.getCollectionObject()
        s.w(f"public {self.Class.SetDescription} fromList(ArrayList<{self.Class.Name}> {self.Class.Name.lower()}List) ").o()
        #s.wln(f"this._data = new {JavaCollectionObject}();")
        s.wln(f"this._data = new TreeMap<>();")
        s.w(f"for ({self.Class.Name} _{self.Class.Name.lower()} : {self.Class.Name.lower()}List)").o()
        s.wln(f"this._data.put(_{self.Class.Name.lower()}.get{pkproperty.Name}(), _{self.Class.Name.lower()});").c()
        s.wln("return this;").c().ret()
        return s

    def writeClassCollectionToList(self, s:JavaStringWriter):
        s.w(f"public ArrayList<{self.Class.Name}> toList() ").o()
        s.wln(f"ArrayList<{self.Class.Name}> arr = new ArrayList<{self.Class.Name}>(this._data.values());")
        s.wln(f"return arr;").c().ret()
        return s 
    
    def writeClassCollectionToDictionary(self, s:JavaStringWriter):
        #pkcls = self.getPrimaryKeyClass()
        #JavaCollectionObject = self.getCollectionObject()
        dictObject =  self.getCollectionObject("Map")
        s.w(f"public {dictObject} toDict() ").o()
        s.wln(f"{dictObject} dict = new HashMap<>(this._data);")
        s.wln(f"return dict;").c().ret()
        return s

    def writeClassCollectionFromDictionary(self, s:JavaStringWriter):
        JavaCollectionObject = self.getCollectionObject()
        dictObject =  self.getCollectionObject("Map")
        s.w(f"public {self.Class.SetDescription} fromDict({dictObject} dict) ").o()
        s.wln(f"this._data = new TreeMap<>(dict);")
        s.wln("return this;").c().ret()
        return s 
    
    
    def writeClassCollectionClose(self, s:JavaStringWriter):
        s.c()
        return s  

    def getClassCollectionDependencies(self):
        dependency_map = {}
        
        _sm = "import java.util.SortedMap;"
        _tm = "import java.util.TreeMap;" 
        _al = "import java.util.ArrayList;"
        _hm = "import java.util.HashMap;"
        _mp = "import java.util.Map;"
        ent = self.Class.ParentModule.ParentProject.Entity.lower()
        proj = self.Class.ParentModule.ParentProject.Name.lower()
        modl = self.Class.ParentModule.Name.lower()
        clss = self.Class.Name
        _cls = f"import {ent}.{proj}.{modl}.{clss};"

        pkproperty = self.getPrimaryKeyProperty()
        if pkproperty is not None:
            for dependency in pkproperty.Java_Dependencies():
                if dependency not in dependency_map:
                    dependency_map[dependency] = dependency

        dependency_map[_sm] = _sm
        dependency_map[_tm] = _tm
        dependency_map[_al] = _al
        dependency_map[_hm] = _hm
        dependency_map[_mp] = _mp
        #dependency_map[_cls] = _cls

        return dependency_map
    
