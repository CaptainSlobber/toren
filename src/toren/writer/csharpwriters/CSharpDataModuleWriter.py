import collections
import json
import os
from pathlib import Path

from typing import List

from ...datastores.Database import Database
from ..DataModuleWriter import DataModuleWriter
from .CSharpClassWriter import CSharpClassWriter
from .CSharpDataClassWriter import CSharpDataClassWriter
from .CSharpStringWriter import CSharpStringWriter
from ...Project import Project
from ...Module import Module

from ...languages import *
from ...tracer.Logger import Logger

class CSharpDataModuleWriter(DataModuleWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         language=language, 
                         database=database,
                         logger=logger)
        self.Project = project
        self.Module = module
        self.Language = language
        self.Database = database
        self.ClassWriterClass = CSharpClassWriter
        self.DataClassWriterClass = CSharpDataClassWriter
        self.StringWriterClass = CSharpStringWriter
        self.HeaderFileName = f"{self.Module.Name}"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.AdminFunctionsClassName = "Admin"
        self.FilterObjectClassName = "Filter"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def getDataDependencies(self):
        dependency_map = {}
        for dependency in self.Database.CSharpDependencies():
            dependency_map[dependency] = dependency
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            #dependency_map[class_dep] = class_dep
        
        return dependency_map
    
    def writeDLPackage(self, s:CSharpStringWriter):
        p = self.Module.ParentProject.Name
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD
        s.wln(f"namespace {e}.{p}.{m}.{b};")
        s.ret()
        return s
    

    def getDatalayerModuleName(self):
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD.lower()
        dlmodule = f"{e.lower()}.{p.lower()}.{self.Module.Name.lower()}.{self.Database.Name.lower()}"
        return dlmodule
    
    def getDataModulePath(self) -> str:
        dbmod = self.getDatalayerModuleName()

        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                dbmod)

        return data_module_path
    

    def writeDataLayerModuleObjects(self, classes):
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        dbmod = f"{m.lower()}.{b.lower()}"
        mDataLayer = Module().initialize(name=dbmod, 
                               description=dbmod, 
                               id="1095d1dd-3c3b-4005-b6c3-9dd9a025743a",
                               classes=classes)
        mDataLayer.setParentProject(self.Project)

        for classid, _class in mDataLayer.Classes.Data.items():
            c = self.ClassWriterClass(project=self.Project,
                          module=mDataLayer,
                          class_=_class,
                          language=self.Language,
                          logger=self.Logger)
            c.write()
        return mDataLayer

    
    def writeOpenCommonDataFunctions(self, classname: str, s:CSharpStringWriter):
        
        s.ret()

        s.write(f"public class {classname} ").o()

        s.wln("/*")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Datalayer Functions")
        s.wln("*/")
        s.ret()

        
        return s
    
    def writeCommonCreateConnection(self, s:CSharpStringWriter):
        db = self.Database
        connclass = db.ConnectionClass(self.Language)
        conobjclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        s.w(f"public static {connclass} GetConnection({conobjclass} config) ").o()
        s.wln(f"{connclass} connection = null;")
        s = db.WriteConnectionInitialization(self.Language, s)    
        s.wln("return connection;")
        s.c()
        s.ret()
        return s
    
    def writeCloseCommonDataFunctions(self, s:CSharpStringWriter):
        s.c()
        s.ret()
        
        return s


    def writeOpenCommonAdminFunctions(self, classname: str, s:CSharpStringWriter):
        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            class_dep = f"{dlclassname}"
            #s.wln(class_dep)    
        s.ret()
        s.write(f"public class {classname} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Admin Functions")
        s.wln("*/")
        s.ret()
        
        return s

    def writeCloseCommonAdminFunctions(self, s:CSharpStringWriter):
        s.c()
        s.ret()
        
        return s
    
    
    def writeCommonSetupConnection(self, s:CSharpStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"

        connclass = db.ConnectionClass(self.Language)
        s.wln(f"{connclass} connection = {cfn}.GetConnection(config);")

        return s
    
    def writeCommonHandleQueryException(self, s:CSharpStringWriter): 
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        exceptionclass = db.SQLExceptionClass(self.Language)
        s.w(f"public static void Handle{exceptionclass}({exceptionclass} e) ").o()
        s.wln("Console.WriteLine(e.ToString());")
        s.c()
        s.ret()
        return s

    def writeCommonExecuteParameterizedNonQuery(self, s:CSharpStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        connclass = db.ConnectionClass(self.Language)
        conobjclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        commandclass = db.CommandClass(self.Language)

        s.w(f"public static int ExecuteParameterizedNonQuery({conobjclass} config, string query, Dictionary<string, Dictionary<string, object>> parameters) ").o()
        s.wln(f"int rowsAffected = 0;")
        s.w(f"using ({connclass} connection = {cfn}.GetConnection(config))").o()
        s.w(f"using ({commandclass} command = new {commandclass}(query, connection))").o()
        s.w("try ").o()
        s.wln("connection.Open();")
        if db.Name.lower() == "oracle":
            s.wln("command.BindByName = true;")
        s.w("foreach (var paramater in parameters)").o()
        s.wln("var dbtype = paramater.Value[\"DbType\"]; ")
        s.wln("var value = paramater.Value[\"Value\"];")
        if db.Name.lower() == "oracle": # Oracle requires the OracleDbType to be specified for each parameter
            s.wln("command.Parameters.Add(paramater.Key, (OracleDbType) dbtype).Value = value;")
        else:
            s.wln("command.Parameters.AddWithValue(paramater.Key, value);")
        s.c()
        s.wln("rowsAffected = command.ExecuteNonQuery();")
        s = self.closeTry(s)
        s.c()
        s.c()
        s.wln(f"return rowsAffected;")
        s.c()
        s.ret()

        return s
    
    
    def closeTry(self, s: CSharpStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        exceptionclass = db.SQLExceptionClass(self.Language)
        s.b(f" catch ({exceptionclass} e) ")
        s.wln(f"{cfn}.Handle{exceptionclass}(e);")
        s.c()
        return s

    def writeCommonExecuteNonQuery(self, s:CSharpStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        connclass = db.ConnectionClass(self.Language)
        commandclass = db.CommandClass(self.Language)
        exceptionclass = db.SQLExceptionClass(self.Language)
        conobjclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"

        s.w(f"public static int ExecuteNonQuery({conobjclass} config, string query) ").o()
        s.wln(f"int rowsAffected = 0;")
        s.w(f"using ({connclass} connection = {cfn}.GetConnection(config))").o()
        s.w(f"using ({commandclass} command = new {commandclass}(query, connection))").o()
        s.w("try ").o()
        s.wln("connection.Open();")
        s.wln("rowsAffected = command.ExecuteNonQuery();")
        s = self.closeTry(s)
        s.c()
        s.c()
        s.wln(f"return rowsAffected;")
        s.c()
        s.ret()

        s.w(f"public static int ExecuteNonQueries({conobjclass} config, string[] queries) ").o()
        s.wln(f"int rowsAffected = 0;")
        s.w(f"using ({connclass} connection = {cfn}.GetConnection(config))").o()
        s.w(f"for (int i = 0; i < queries.Length; i++) ").o()
        s.w(f"using ({commandclass} command = new {commandclass}(queries[i], connection))").o()
        s.w("try ").o()
        s.wln("connection.Open();")
        s.wln("rowsAffected += command.ExecuteNonQuery();")
        s = self.closeTry(s)
        s.c()
        s.c()
        s.c()
        s.wln("return rowsAffected;")
        s.c()
        s.ret()
        return s

   
    
    def writeCommonCleanupConnection(self, s:CSharpStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        exceptionclass = db.SQLExceptionClass(self.Language)
        s.w("try ").o()
        s.wln(f"connection.Close();")
        s.b(f" catch ({exceptionclass} e) ")
        s.wln(f"{cfn}.Handle{exceptionclass}(e);")
        s.c()
        return s