import collections
import json
import os
from pathlib import Path

from typing import List
from ..datatypes.DatatypeInt import DatatypeInt
from ..datatypes.DatatypeNetworkAddress import DatatypeNetworkAddress
from ..datatypes.DatatypeString import DatatypeString
from ..datastores.Database import Database
from .WriterObject import WriterObject
from .ClassWriter import ClassWriter
from .DataClassWriter import DataClassWriter
from .StringWriter import StringWriter
from ..Project import Project
from ..Module import Module
from ..Class import Class

from ..languages import *
from ..tracer.Logger import Logger

class DataModuleWriter(WriterObject):

    def __init__(self, project: Project, 
                 module: Module, 
                 language: Language, 
                 database: Database,
                 logger:Logger=None):
        super().__init__()
        self.Project = project
        self.Module = module
        self.Language = language
        self.Database = database
        self.ClassWriterClass = ClassWriter
        self.DataClassWriterClass = DataClassWriter
        self.StringWriterClass = StringWriter
        self.HeaderFileName = f"{self.Module.Name}_header"
        self.ConnectionObjectClassName = "Connection"
        self.CommonFunctionsClassName = "Common"
        self.AdminFunctionsClassName = "Admin"
        self.FilterObjectClassName = "Filter"
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def getDatalayerModuleName(self):
        return f"{self.Module.Name.lower()}_{self.Database.Name.lower()}"
    
    def getDataModulePath(self) -> str:
        dbmod = self.getDatalayerModuleName()

        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                self.Project.Name, 
                                                dbmod)
        return data_module_path
    
    def write(self):
        self.Logger.Log(f"=> Writing Data Module: {self.Module.Name}")
        data_module_path = self.getDataModulePath()
        self.Logger.Log(f"=> To Path: {data_module_path}")
        self.writeDirectory(data_module_path, clear=True)



        headerfn = f"{self.HeaderFileName}.{self.Language.DefaultFileExtension}"
        self.writeDataModuleHeader(data_module_path, headerfn)

        flt = f"{self.getDLPrefix()}{ self.FilterObjectClassName}{self.getDLSuffix()}"
        con = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        cfn = f"{self.getDLPrefix()}{ self.CommonFunctionsClassName}{self.getDLSuffix()}"
        afn = f"{self.getDLPrefix()}{ self.AdminFunctionsClassName}{self.getDLSuffix()}"
        co = self.getConnectionObject(con)
        fo = self.getFilterObject(flt)
        self.writeDataLayerModuleObjects([co, fo])
        self.writeCommonDataFunctions(data_module_path, cfn)
        self.writeConmmonAdminFunctions(data_module_path, afn)
        for classid, _class in self.Module.Classes.Data.items():
            dlclassname = f"{self.getDLPrefix()}{ _class.Name}{self.getDLSuffix()}"
            c = self.DataClassWriterClass(project=self.Project,
                          module=self.Module,
                          class_=_class,
                          language=self.Language,
                          database=self.Database,
                          dlclassname=dlclassname,
                          connectionobjectclassname=con,
                          commonfunctionsclassname=cfn,
                          filterobjectclassname=flt,
                          logger=self.Logger)
            c.write()


    def getDLPrefix(self):
        return "DL"
    
    def getDLSuffix(self):
        return ""
    
    def writeDataModuleHeader(self, path, filename):
        s = self.S
        for classid, _class in self.Module.Classes.Data.items():
            pass


    def getFilterObject(self, filterobjectclassname):
        #s = self.S
        #s.clear()
        #filterobjectclassname = f"{self.getDLPrefix()}{ self.FilterObjectClassName}{self.getDLSuffix()}"
        pPropertyName = DatatypeString().initialize(name="PropertyName",
                                               description="FilterObject.PropertyName",
                                               id="cb4f6960-9101-4d06-ae42-8dc398736813",
                                               isprimarykey=True)
        
        pComparator = DatatypeString().initialize(name="Comparator",
                                               description="FilterObject.Comparator",
                                               id="1cd7107e-c177-4182-a1d8-579e4be0f6ac")
        
        pCompareTo = DatatypeString().initialize(name="CompareTo",
                                               description="FilterObject.CompareTo",
                                               id="cb750a06-c187-4e9b-be98-fbd35ec60b7c")
        
        properties = [pPropertyName, pComparator, pCompareTo]
        cFilterObject = Class().initialize(name=filterobjectclassname, 
                               description=filterobjectclassname, 
                               id="d7486935-70c3-431f-92a5-6e648d5dd115",
                               properties=properties)
        
        return cFilterObject
        

    def writeDataLayerModuleObjects(self, classes):
        dbmod = self.getDatalayerModuleName()
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

    def getConnectionObject(self, connectionobjectclassname):


        pServer = DatatypeString().initialize(name="Server",
                                               description="ConnectionObject.Server",
                                               id="62ce3bc2-3069-4a3c-beff-dc89a5bafaf7")
        pInstanceName = DatatypeString().initialize(name="InstanceName",
                                               description="ConnectionObject.InstanceName",
                                               id="58c88553-a591-4f43-b7a5-8096b35dcfae")
        pServerAddress = DatatypeNetworkAddress().initialize(name="ServerAddress",
                                               description="ConnectionObject.ServerAddress",
                                               id="19e68a2b-7723-4a51-8807-876425ca88dd",
                                               defaultvalue="0.0.0.0")
        pPortNumber = DatatypeInt().initialize(name="PortNumber",
                                               description="ConnectionObject.PortNumber",
                                               id="8f6ac32f-b815-4348-94c4-8123d7c0ea52")
        pUsername = DatatypeString().initialize(name="Username",
                                               description="ConnectionObject.Username",
                                               id="7a7d233d-800c-49d0-9792-f240181f7e7f")
        pCredential = DatatypeString().initialize(name="Credential",
                                               description="ConnectionObject.Credential",
                                               id="e8f482b8-0649-41cd-88f9-727bbc030799")
        pServiceName = DatatypeString().initialize(name="ServiceName",
                                               description="ConnectionObject.ServiceName",
                                               id="9ecf2e46-7b6c-4883-9903-5c255a21dad7")
        pDriver = DatatypeString().initialize(name="Driver",
                                               description="ConnectionObject.Driver",
                                               id="69e4dd5d-68c5-45fb-b138-88e77ec6ca73")
        pConnectionString = DatatypeString().initialize(name="ConnectionString",
                                               description="ConnectionObject.ConnectionString",
                                               id="380ffa83-aa37-4391-bf70-44c3cba825fc",
                                               maxlength=1024,
                                               isprimarykey=True)
        pDatabase = DatatypeString().initialize(name="Database",
                                               description="ConnectionObject.Database",
                                               id="e1753cf9-7c89-41cb-a47a-987e8e69a5b1")
        pDataPath = DatatypeString().initialize(name="DataPath",
                                               description="ConnectionObject.DataPath",
                                               id="823b1b84-2b90-43ff-930d-9ad4bce39d67",
                                               maxlength=1024)
        
        properties = [pServer, pInstanceName, pServerAddress, pPortNumber, pUsername, pCredential, 
                      pServiceName, pDriver, pDatabase, pConnectionString, pDataPath]
        cConnectionObject = Class().initialize(name=connectionobjectclassname, 
                               description=connectionobjectclassname, 
                               id="4ed850e3-f9f9-4dc7-aa79-9e6a310b4ebc",
                               properties=properties)
        
        return cConnectionObject
        


    def writeConmmonAdminFunctions(self, path, classname):
        s = self.S
        s.clear()
        s = self.writeDLPackage(s)
        ad = f"{self.getDLPrefix()}{ self.AdminFunctionsClassName}{self.getDLSuffix()}"
        dependency_map = self.getDataDependencies()
        s = self.writeDataDependencies(dependency_map, s)
        s = self.writeOpenCommonAdminFunctions(classname, s)
        s = self.writeCheckSchemaExistence(s)
        s = self.writeCreateSchema(s)
        s = self.writeCreateAllTables(s)
        s = self.writeDropAllTables(s)  
        s = self.writeClearAllTables(s)

        s = self.writeCloseCommonAdminFunctions(s)


        filename = f"{classname}.{self.Language.DefaultFileExtension}"
        self.writeFile(path, filename, s.toString())

    def writeCommonDataFunctions(self, path, classname):
        s = self.S
        s.clear()
        
        s = self.writeDLPackage(s)

        conclass = f"{self.getDLPrefix()}{ self.ConnectionObjectClassName}{self.getDLSuffix()}"
        dependency_map = self.getDataDependencies()
        s = self.writeDataDependencies(dependency_map, s)
        s = self.writeOpenCommonDataFunctions(classname, s)

        s = self.writeCommonCreateConnection(s)
        s = self.writeCommonHandleQueryException(s)
        s = self.writeCommonExecuteNonQuery(s)
        s = self.writeCommonExecuteParameterizedNonQuery(s)
        s = self.writeCommmonFetchOne(s)
        s = self.writeCommonFetchAll(s)

        s = self.writeCloseCommonDataFunctions(s)

        filename = f"{classname}.{self.Language.DefaultFileExtension}"
        self.writeFile(path, filename, s.toString())

    def getSchema(self):
        db = self.Database
        if db.HasSchema():
            return f"{db.OB()}{self.Module.Name}{db.CB()}."
        return ""

    def writeDLPackage(self, s:StringWriter):
        return s

    def writeCreateAllTables(self, s:StringWriter):
        return s
    
    def writeDropAllTables(self, s:StringWriter):
        return s
    
    def writeClearAllTables(self, s:StringWriter):
        return s

    def writeOpenCommonAdminFunctions(self, classname: str, s:StringWriter):
        return s
    
    def writeOpenCommonDataFunctions(self, classname: str, s:StringWriter):
        return s
    
    def writeCloseCommonDataFunctions(self, s:StringWriter):
        return s
    
    def writeCloseCommonAdminFunctions(self, s:StringWriter):
        return s
        
    def writeCommonCreateConnection(self, s:StringWriter): 
        return s
    
    def writeCommonHandleQueryException(self, s:StringWriter): 
        return s
    
    def writeCommonExecuteNonQuery(self, s:StringWriter):
        return s
    
    def writeCommonExecuteParameterizedNonQuery(self, s:StringWriter):
        return s
    
    def writeCommmonFetchOne(self, s:StringWriter):
        return s
    
    def writeCommonFetchAll(self, s:StringWriter):
        return s

    def writeCheckSchemaExistence(self, s:StringWriter):
        return s
    
    def writeCreateSchema(self, s:StringWriter):
        schema = self.getSchema()

        return s

    def getDataDependencies(self):
        dependency_map = {}
        return dependency_map


    def writeDataDependencies(self, dependency_map, s:StringWriter):
        
        for dependencyid, dependency in dependency_map.items():
            s.wln(f"{dependency}")
        
        s.ret()
        return s
