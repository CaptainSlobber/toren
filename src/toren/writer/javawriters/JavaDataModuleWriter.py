import collections
import json
import os
from pathlib import Path

from typing import List
from ...datastores.Database import Database
from ..DataModuleWriter import DataModuleWriter
from .JavaClassWriter import JavaClassWriter
from .JavaDataClassWriter import JavaDataClassWriter
from .JavaStringWriter import JavaStringWriter
from ...Project import Project
from ...Module import Module

from ...languages import *
from ...tracer.Logger import Logger

class JavaDataModuleWriter(DataModuleWriter):

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
        self.ClassWriterClass = JavaClassWriter
        self.DataClassWriterClass = JavaDataClassWriter
        self.StringWriterClass = JavaStringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.FilterObjectClassName = "Filter"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def getDataDependencies(self):
        dependency_map = {}
        for dependency in self.Database.JavaDependencies():
            dependency_map[dependency] = dependency
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            #dependency_map[class_dep] = class_dep
        
        return dependency_map
    


    def writeDLPackage(self, s:JavaStringWriter):
        p = self.Module.ParentProject.Name
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD
        s.wln(f"package {t}.{e}.{p}.{m}.{b};")
        #s.wln(f"package {m}_{b};")
        s.ret()
        return s

    def writeOpenCommonDataFunctions(self, classname: str, s:JavaStringWriter):
        
        s.wln(f"import java.nio.charset.StandardCharsets;")
        s.wln(f"import java.util.Base64;")
        s.ret()

        s.write(f"public class {classname} ").o()

        s.wln("/*")
        s.wln(f" Class: {classname}")
        s.wln(f" Description: Common Datalayer Functions")
        s.wln("*/")
        s.ret()

        
        return s
    
    def writeCommonCreateConnection(self, s:JavaStringWriter):
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
    
    def writeCloseCommonDataFunctions(self, s:JavaStringWriter):
        s.c()
        s.ret()
        
        return s


    def writeOpenCommonAdminFunctions(self, classname: str, s:JavaStringWriter):
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
    
    def getDatalayerModuleName(self):
        return f"{self.Module.Name.lower()}.{self.Database.Name.lower()}"
    
    def getDataModulePath(self) -> str:
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD.lower()
        src = "src"
        main = "main"
        java = "java"
        dbmod = f"{self.Module.Name.lower()}.{self.Database.Name.lower()}"

        data_module_path = os.path.join(self.Language.OutputDirectory, p, dbmod, src, main, java, t, e, p, m, b)
        self.writeDirectory(data_module_path, True)
        return data_module_path

    def writeCloseCommonAdminFunctions(self, s:JavaStringWriter):
        s.c()
        s.ret()
        
        return s
    
    
    def writeCommonSetupConnection(self, s:JavaStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"

        connclass = db.ConnectionClass(self.Language)
        s.wln(f"{connclass} connection = {cfn}.GetConnection(config);")
        #s.wln(f"connection.setAutoCommit(false);")
        return s
    
    def writeCommonHandleQueryException(self, s:JavaStringWriter): 

        s.w(f"public static void HandleSQLException(SQLException e) ").o()
        s.wln("e.printStackTrace();")
        s.c()
        s.ret()
        return s

    def writeCommonExecuteParameterizedNonQuery(self, s:JavaStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        connclass = db.ConnectionClass(self.Language)
        conobjclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"

        s.w(f"public static Integer ExecuteParameterizedNonQuery(Connection connection, PreparedStatement statement) ").o()
        s.wln("int rowsAffected = 0;")
        s.w("try ").o()

        s.wln("rowsAffected = statement.executeUpdate();")
        s.wln("connection.commit();")
        s = self.closeTry(s)
        s = self.writeCommonCleanupConnection(s)
        s.wln("return rowsAffected;")
        s.c()
        s.ret()


        return s
    
  
    def closeTry(self, s: JavaStringWriter):
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        s.b(f" catch (SQLException e) ")
        s.wln(f"{cfn}.HandleSQLException(e);")
        s.c()
        return s

    def writeCommonExecuteNonQuery(self, s:JavaStringWriter):
        db = self.Database
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        connclass = db.ConnectionClass(self.Language)
        conobjclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"

        s.w(f"public static Integer ExecuteNonQuery({conobjclass} config, String query) ").o()
        s.wln(f"String[] queries = {{ query }};")
        s.wln(f"return {cfn}.ExecuteNonQueries(config, queries);")
        s.c()
        s.ret()

        s.w(f"public static Integer ExecuteNonQueries({conobjclass} config, String[] queries) ").o()
        s = self.writeCommonSetupConnection(s)
        s.wln("int rowsAffected = 0;")
        s.w("try ").o()
        s.w("for (int i=0; i<queries.length; i++) ").o()
        s.wln("PreparedStatement statement = connection.prepareStatement(queries[i]);")
        s.wln(f"rowsAffected += statement.executeUpdate();")
        s.wln(f"connection.commit();")
        s.c()
        s = self.closeTry(s)
        s = self.writeCommonCleanupConnection(s)
        s.wln("return rowsAffected;")
        s.c()
        s.ret()
        return s
    
    def writeCommonCleanupConnection(self, s:JavaStringWriter):
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        s.w("try ").o()
        s.wln(f"connection.close();")
        s.b(" catch (SQLException e) ")
        s.wln(f"{cfn}.HandleSQLException(e);")
        s.c()
        return s