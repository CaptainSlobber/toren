import collections
import json
import os
from pathlib import Path

from typing import List
from ..WriterObject import WriterObject
from ..PropertyWriter import PropertyWriter
from ..StringWriter import StringWriter
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class CSharpDataClassWriter(WriterObject):

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
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)

    def writeDLClassOpen(self, s:StringWriter):

        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        l = self.getDatalayerName()
        c = self.Class.Name
        d = self.getDLClassName()
        s.wln(f"namespace {p}.{l}.{m};")
        s.ret()
        s.write(f"public class {d} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" Data Layer Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("*/")
        s.ret()
        return s
    
    def writeParentClassInitializer(self, s:StringWriter):
        return s

    def writeDLClassInitializer(self, s:StringWriter):
        d = self.getDLClassName()
        s.wln(f"public {d}() {{}}")
        return s
    
    
    def writeCreateTable(self, s:StringWriter):
        return s
    
    def writeInsert(self, s:StringWriter):
        return s
    
    def writeInsertCollection(self, s:StringWriter):
        return s
    
    def writeUpdate(self, s:StringWriter):
        return s
    
    def writeDelete(self, s:StringWriter):
        return s
    
    def writeSelectSingleRecordByPK(self, s:StringWriter):
        return s
    
    def writeSelectWhere(self, s:StringWriter):
        return s

    def writeDLClassClose(self, s:StringWriter):
        s.c()
        return s