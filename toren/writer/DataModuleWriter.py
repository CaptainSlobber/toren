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
        self.S = self.StringWriterClass(self.Language)
        self.setLogger(logger)


    def getDatalayerModuleName(self):
        return f"{self.Module.Name.lower()}_{self.Database.Name.lower()}"
    
    def write(self):
        self.Logger.Log(f"=> Writing Data Module: {self.Module.Name}")
        dbmod = self.getDatalayerModuleName()
        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                self.Project.Name, 
                                                dbmod)
        self.writePath(data_module_path)



        headerfn = f"{self.HeaderFileName}.{self.Language.DefaultFileExtension}"
        self.writeModuleHeader(data_module_path, headerfn)

        self.writeConnectionObject(data_module_path, "DLConnectionObject")
        for classid, _class in self.Module.Classes.Data.items():
            c = self.DataClassWriterClass(project=self.Project,
                          module=self.Module,
                          class_=_class,
                          language=self.Language,
                          database=self.Database,
                          logger=self.Logger)
            c.write()

    def writeModuleHeader(self, path, filename):
        s = self.S
        for classid, _class in self.Module.Classes.Data.items():
            pass

    def writeConnectionObject(self, path, connectionobjectclassname):
        s = self.S

        cofn = f"{connectionobjectclassname}.{self.Language.DefaultFileExtension}"

        

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
        pPassword = DatatypeString().initialize(name="Password",
                                               description="ConnectionObject.Password",
                                               id="e8f482b8-0649-41cd-88f9-727bbc030799")
        pConnectionString = DatatypeString().initialize(name="ConnectionString",
                                               description="ConnectionObject.ConnectionString",
                                               id="380ffa83-aa37-4391-bf70-44c3cba825fc",
                                               maxlength=1024,
                                               isprimarykey=True) # ?
        pDataPath = DatatypeString().initialize(name="DataPath",
                                               description="ConnectionObject.DataPath",
                                               id="823b1b84-2b90-43ff-930d-9ad4bce39d67",
                                               maxlength=1024)
        
        properties = [pServer, pInstanceName, pServerAddress, pPortNumber, pUsername, pPassword, pConnectionString, pDataPath]
        cConnectionObject = Class().initialize(name=connectionobjectclassname, 
                               description=connectionobjectclassname, 
                               id="4ed850e3-f9f9-4dc7-aa79-9e6a310b4ebc",
                               properties=properties)
        
        dbmod = self.getDatalayerModuleName()
        mDataLayer = Module().initialize(name=dbmod, 
                               description=dbmod, 
                               id="1095d1dd-3c3b-4005-b6c3-9dd9a025743a",
                               classes=[cConnectionObject])
        mDataLayer.setParentProject(self.Project) #
        
        c = self.ClassWriterClass(project=self.Project,
                          module=mDataLayer,
                          class_=cConnectionObject,
                          language=self.Language,
                          logger=self.Logger)
        c.write()

    def writeCommon(self, path, filename):
        s = self.S
        pass
