import collections
import json
import os
from pathlib import Path

from typing import List
from ..DataClassWriter import DataClassWriter
from .PythonStringWriter import PythonStringWriter
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...datatypes import *
from ...tracer.Logger import Logger

class PythonDataClassWriter(DataClassWriter):

    def __init__(self, project: Project, 
                 module: Module, 
                 class_: Class,
                 language: Language, 
                 database: Database,
                 dlclassname: str,
                 connectionobjectclassname: str,
                 commonfunctionsclassname: str,
                 filterobjectclassname: str,
                 logger:Logger=None):
        super().__init__(project=project, 
                         module=module, 
                         class_=class_, 
                         database=database,
                         language=language,
                         dlclassname=dlclassname, 
                         connectionobjectclassname=connectionobjectclassname,
                         commonfunctionsclassname=commonfunctionsclassname,
                         filterobjectclassname=filterobjectclassname,
                         logger=logger)
        self.Project = project
        self.Module = module
        self.StringWriterClass = PythonStringWriter
        self.Class = class_
        self.DLCLassName = dlclassname
        self.ConnectionObjectClassName = connectionobjectclassname
        self.CommonFunctionsClassName = commonfunctionsclassname
        self.FilterObjectClassName = filterobjectclassname
        self.Database = database
        self.Language = language
        self.ParentClassName = self.getParentClassName()
        self.setLogger(logger)
        self.S = self.StringWriterClass(self.Language)



    def getDLDependencies(self):
        dependency_map = {}
        for propertyid, property in self.Class.Properties.Data.items():
            for dependency in property.Python_Dependencies():
                if dependency not in dependency_map:
                    dependency_map[dependency] = dependency

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                for dependency in property.Python_Dependencies():
                    if dependency not in dependency_map:
                        dependency_map[dependency] = dependency

        for dependency in self.Database.PythonDependencies():
            dependency_map[dependency] = dependency

        if self.Class.Cloneable:
            dependency_map["import uuid"] = "import uuid"
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        

        return dependency_map

    def writeDLClassOpen(self, s:PythonStringWriter):

        p = self.Class.ParentModule.ParentProject.Name
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name
        b = self.Database.Name.lower()
        c = self.Class.Name
        coll = self.Class.SetDescription
        d = self.getDLClassName()

        con = self.ConnectionObjectClassName
        cfn = self.CommonFunctionsClassName

        s.wln(f"from ..{m}.{coll} import {coll}")
        s.wln(f"from ..{m}.{c} import {c}")
        s.wln(f"from .{con} import {con}")
        s.wln(f"from .{cfn} import {cfn}")
        s.ret()
        s.write(f"class {d}:").o()
        s.ret()
        s.wln("\"\"\"")
        s.wln(f" {self.Database.Name} Data Layer for Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("\"\"\"")
        s.ret()

        return s
    
    def writeParentClassInitializer(self, s:PythonStringWriter):
        return s

    def writeDLClassInitializer(self, s:PythonStringWriter):
        d = self.getDLClassName()
        s.wln("def __init__(self):").o()
        s.wln(f"pass")
        s.c()
        s.ret()
        return s
    
    def writeDLClassProperties(self, s:PythonStringWriter):
        s.wln(f'SCHEMA_NAME = "{self.Class.ParentModule.Name}"')
        s.wln(f'TABLE_NAME = "{self.Class.Name}"')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s.wln(f'COL_NAME_{property.Name.upper()} = "{property.Name}"')
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f'COL_NAME_{property.Name.upper()} = "{property.Name}"')
        s.ret()
        return s
    

    def writeCreateTableColumn(self, s:PythonStringWriter, property):
        db = self.Database
        NOTNULL = " NOT NULL"
        if property.AllowNulls:
            NOTNULL = ""
        PRIMARYKEY = ""
        if property.IsPrimaryKey: 
            PRIMARYKEY = " PRIMARY KEY"
        UNIQUE = ""
        if property.IsUnique:
            UNIQUE = " UNIQUE"
        DATATYPE = property.DatabasePropertyType(db)
        
        s.wln(f'createquery += "{db.OB()}{property.Name}{db.CB()} {DATATYPE}{NOTNULL}{UNIQUE}{PRIMARYKEY},"')
        return s


    def getInstanceIDParameter(self, prefix: str = ""):
        if self.Class.Cloneable:
            return prefix + self.getInstanceIDParemeterName() + ": uuid.UUID=None"
        else:
            return ""
    
    def  getInstanceIDParemeterName(self, prefix: str = ""):
        if self.Class.Cloneable:
            return prefix + "instanceID"
        else:
            return ""
        
    def  getInstanceIDExt(self):
        if self.Class.Cloneable:
            return "{" + self.getInstanceIDParemeterName() + "Str" + "}"

        else:
            return ""
    

    def writeInstanceStr(self, s:PythonStringWriter, iq:str ="innerquery"):
        iin2 = self.getInstanceIDParemeterName(", ")
        if self.Class.Cloneable:
            s.wln(f"innerquery = {self.getDLClassName()}.GetInnerQuery({iq}{iin2})")
        else:
            s.wln(f"innerquery = {self.getDLClassName()}.GetInnerQuery({iq})")
        return s

    def writeCreateTable(self, s:PythonStringWriter):
        db = self.Database
        iin = self.getInstanceIDParemeterName()
        iid = self.getInstanceIDParameter()
        iid2 = self.getInstanceIDParameter(", ")
        iie = self.getInstanceIDExt()
        schema = self.getSchema()
        tablename = db.GetTableName(self.Class)


        if self.Class.Cloneable:
            s.wln("@staticmethod")
            s.wln(f'def GetInnerQuery(innerquery: str="{tablename}"{iid2}):').o()
            s.wln(f"if {iin} is not None:").o()
            s.wln(f"if isinstance({iin}, uuid.UUID):").o()
            s.wln(f"id = str({iin})")
            s.wln(f'return f"{db.GetTableName(self.Class, "{id}")}"')     
            s.c().c()
            s.wln(f'return innerquery')
            s.c()
            s.ret()
        else:
            s.wln("@staticmethod")
            s.wln(f'def GetInnerQuery(innerquery: str="{tablename}"):').o()
            s.wln(f'return innerquery')
            s.c()
            s.ret()

        s.wln("@staticmethod")
        s.wln(f"def GetCreate{self.Class.Name}TableQuery({iid}):").o()

        s = self.writeInstanceStr(s, "\"" + tablename + "\"")
        s.wln(f'createquery = f"CREATE TABLE{db.IfNotExists()} {{innerquery}} ("')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s = self.writeCreateTableColumn(s, property)
        for propertyid, property in self.Class.Properties.Data.items():
            s = self.writeCreateTableColumn(s, property)

        if not db.SeparateForeignKeyCreation():
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if property.ForeignKey is not None:
                        create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "{innerquery}")
                        s.wln(f'createquery += "{create_fk},"')
            for propertyid, property in self.Class.Properties.Data.items():
                if property.ForeignKey is not None:
                    create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "{innerquery}")
                    s.wln(f'createquery += "{create_fk},"')
        
        s.wln(f'createquery = createquery[:-1] + "){db.EndQuery()}"')
        s.wln("return createquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def Create{self.Class.Name}Table(config{iid2}):").o()
        s.wln(f"createquery = {self.getDLClassName()}.GetCreate{self.Class.Name}TableQuery({iin})")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, createquery)")
        s.c()
        s.ret()
        return s
    
    def checkTableExistence(self, s:PythonStringWriter):
        return s
    

    def getCommonItems(self):
        db = self.Database
        iin = self.getInstanceIDParemeterName()
        iin2 = self.getInstanceIDParemeterName(", ")

        iid = self.getInstanceIDParameter()
        iid2 = self.getInstanceIDParameter(", ")
        schema = self.getSchema()
        tablename = db.GetTableName(self.Class)

        return (db, schema, tablename, iid, iid2, iin, iin2)

    def writeClearTable(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        s.wln("@staticmethod")
        s.wln(f"def GetClear{self.Class.Name}TableQuery({iid}):").o()
        s = self.writeInstanceStr(s, "\"" + tablename + "\"")
        s.wln(f'clearquery = f"DELETE FROM {{innerquery}}{db.EndQuery()}"')
        s.wln("return clearquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def Clear{self.Class.Name}Table(config{iid2}):").o()
        s.wln(f"clearquery = {self.getDLClassName()}.GetClear{self.Class.Name}TableQuery({iin})")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, clearquery)")
        s.c()
        s.ret()
        return s
    
    def writeDropTable(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        s.wln("@staticmethod")
        s.wln(f"def GetDrop{self.Class.Name}TableQuery({iid}):").o()
        #s.writeline(f'innerquery = "{tablename}"')
        s = self.writeInstanceStr(s, "\"" + tablename + "\"")
        s.wln(f'dropquery = f"DROP TABLE{db.IfExists()} {{innerquery}}{db.EndQuery()}"')
        s.wln("return dropquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def Drop{self.Class.Name}Table(config{iid2}):").o()
        s.wln(f"dropquery = {self.getDLClassName()}.GetDrop{self.Class.Name}TableQuery({iin})")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, dropquery)")
        s.c()
        s.ret()
        return s
    
    def writeGetColumnNames(self, s:PythonStringWriter):
        db = self.Database
        columns = []
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        for propertyid, property in self.Class.Properties.Data.items():
            columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        columns_string = ", ".join(columns)
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}ColumnNames():").o()
        s.wln(f'columns = "{columns_string}"')
        s.wln("return columns")
        s.c()
        s.ret()
        return s
    
    
    
    def writeCreateForeignKeys(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        if db.SeparateForeignKeyCreation():
            s.wln("@staticmethod")
            s.wln(f"def Get{self.Class.Name}ForeignKeyQueries({iid}):").o()
            s = self.writeInstanceStr(s, "\"" + tablename + "\"")
            s.wln("foreignkeyqueries = []")
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if property.ForeignKey is not None:
                        create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "{innerquery}")
                        s.wln(f'foreignkeyqueries.append(f"{create_fk}")')
                        

            for propertyid, property in self.Class.Properties.Data.items():
                if property.ForeignKey is not None:
                    create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "{innerquery}")
                    s.wln(f'foreignkeyqueries.append(f"{create_fk}")')
            s.writeline("return foreignkeyqueries")
            s.c()
            s.ret()

            s.wln("@staticmethod")
            s.wln(f"def Create{self.Class.Name}ForeignKeys(config{iid2}):").o()
            s.wln(f"foreignkeyqueries = {self.getDLClassName()}.Get{self.Class.Name}ForeignKeyQueries({iin})")
            s.wln(f"for foreignkeyquery in foreignkeyqueries:").o()
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, foreignkeyquery)")
            s.c()
            s.c()
            s.ret()
        return s
    
    def writeGetColumnParameters(self, s:PythonStringWriter):
        db = self.Database
        params = []
        n = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                n = n + 1
                params.append(f"{db.GetParameter(property.Name.lower(), n)}")
        for propertyid, property in self.Class.Properties.Data.items():
            n = n + 1
            params.append(f"{db.GetParameter(property.Name.lower(), n)}")
        params_string = ", ".join(params)
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}ColumnParameters():").o()
        s.wln(f'params = "{params_string}"')
        s.wln("return params")
        s.c()
        s.ret()
        return s
    
    def writeInsertItem(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}InsertQuery({iid}):").o()
        #s.writeline(f'innerquery = "{tablename}"')
        s = self.writeInstanceStr(s, "\"" + tablename + "\"")
        s.wln(f'columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()')
        s.wln(f"params = {self.getDLClassName()}.Get{self.Class.Name}ColumnParameters()")
        s.wln(f'insertquery = f"INSERT INTO {{innerquery}} ({{columns}}) VALUES ({{params}}){db.EndQuery()}"')
        s.wln("return insertquery")
        s.c().ret()


        s.wln("@staticmethod")
        s.wln(f"def Parameterize{self.Class.Name}({self.Class.Name.lower()}: {self.Class.Name}) -> dict:").o()

        if db.UsesNamedParameters(self.Language):
            s.wln("params = {}")
        else:
            s.wln("params = []")
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                converted = property.To(self.Language, self.Database, f"{self.Class.Name.lower()}.{property.Name}")
                if db.UsesNamedParameters(self.Language):
                    s.wln(f"params['{property.Name.lower()}'] = {converted}")
                else:
                    s.wln(f"params.append({converted})")        
        for propertyid, property in self.Class.Properties.Data.items():
            converted = property.To(self.Language, self.Database, f"{self.Class.Name.lower()}.{property.Name}")
            if db.UsesNamedParameters(self.Language):
                s.wln(f"params['{property.Name.lower()}'] = {converted}")
            else:
                s.wln(f"params.append({converted})")  
        s.wln("return params")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f"def InsertSingle{self.Class.Name}(config, {self.Class.Name.lower()}: {self.Class.Name}{iid2}):").o()
        s.wln(f"params = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()})")
        s.wln(f"insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin})")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, insertquery, params)")
        s.c()
        s.ret()

        return s
    
    def writeInsertCollection(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        s.wln("@staticmethod")
        s.wln(f"def Insert{self.Class.SetDescription}(config, {self.Class.SetDescription.lower()}: {self.Class.SetDescription}{iid2}):").o()
        s.wln(f"{self.Class.Name.lower()}list = {self.Class.SetDescription.lower()}.toList()")
        s.wln(f"return {self.getDLClassName()}.Insert{self.Class.Name}List(config, {self.Class.Name.lower()}list{iin2})")
        s.c()
        
        s.wln("@staticmethod")
        s.wln(f"def Insert{self.Class.Name}List(config, {self.Class.Name.lower()}list: list{iid2}):").o()
        s.wln("data = []")
        s.wln(f"for {self.Class.Name.lower()} in {self.Class.Name.lower()}list:").o()
        s.wln(f"params = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()})")
        s.wln("data.append(params)")
        s.c()
        s.wln(f"insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin})")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteManyParameterizedNonQuery(config, insertquery, data)")
        s.c()
        s.ret()
        return s
    
    def writeUpdate(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()
            s.wln("@staticmethod")
            s.wln(f"def Get{self.Class.Name}UpdateQuery({iid}):").o()
            #s.writeline(f'innerquery = "{tablename}"')
            s = self.writeInstanceStr(s, "\"" + tablename + "\"")
            s.wln(f'updatequery = f"UPDATE {{innerquery}} SET "')
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if not property.IsPrimaryKey:
                        s.wln(f'updatequery += "{db.OB()}{property.Name}{db.CB()} = {db.GetParameter(property.Name.lower())},"')
            for propertyid, property in self.Class.Properties.Data.items():
                if not property.IsPrimaryKey:
                    s.wln(f'updatequery += "{db.OB()}{property.Name}{db.CB()} = {db.GetParameter(property.Name.lower())},"')
            s.wln(f'updatequery += "WHERE {db.OB()}{pk.Name}{db.CB()} = {db.GetParameter(pk.Name.lower())}{db.EndQuery()}"')
            s.wln("return updatequery")
            s.c().ret()

            s.wln("@staticmethod")
            s.wln(f"def UpdateSingle{self.Class.Name}(config, {self.Class.Name.lower()}: {self.Class.Name}{iid2}):").o()
            s.wln(f"params = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()})")
            s.wln(f"updatequery = {self.getDLClassName()}.Get{self.Class.Name}UpdateQuery({iin})")
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, updatequery, params)")
            s.c()
            s.ret()
        return s
    
    def writeDelete(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()
            s.wln("@staticmethod")
            s.wln(f"def Get{self.Class.Name}DeleteQuery({iid}):").o()
            #s.writeline(f'innerquery = "{tablename}"')
            s = self.writeInstanceStr(s, "\"" + tablename + "\"")
            s.wln(f'deletequery = f"DELETE FROM {{innerquery}} WHERE {db.OB()}{pk.Name}{db.CB()} = {db.GetParameter(pk.Name.lower())}{db.EndQuery()}"')
            s.wln("return deletequery")
            s.c().ret()

            s.wln("@staticmethod")
            s.wln(f"def DeleteSingle{self.Class.Name}By{pk.Name}(config, {pk.Name.lower()}{iid2}):").o()
            if db.UsesNamedParameters(self.Language):
                s.wln(f"params = {{ '{pk.Name.lower()}': {pk.Name.lower()} }}")
            else:
                s.wln(f"params = [ {pk.Name.lower()} ]")
            s.wln(f"deletequery = {self.getDLClassName()}.Get{self.Class.Name}DeleteQuery({iin})")
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, deletequery, params)")
            s.c()
            s.ret()

            s.wln("@staticmethod")
            s.wln(f"def DeleteSingle{self.Class.Name}(config, {self.Class.Name.lower()}: {self.Class.Name}{iid2}):").o()
            s.wln(f"{self.getDLClassName()}.DeleteSingle{self.Class.Name}By{pk.Name}(config, {self.Class.Name.lower()}.{pk.Name}{iin2})")
            s.c()
            s.ret()
        return s
    
    def writeSelectSingleRecordByPK(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        data_data_type = "dict"
        #if not db.UsesNamedParameters(self.Language):
        #    data_data_type = "list"
        s.wln("@staticmethod")
        s.wln(f"def Get{self.Class.Name}FromQueryResult(queryresult: {data_data_type}) -> {self.Class.Name}:").o()
        s.wln(f"{self.Class.Name.lower()} = {self.Class.Name}(").o()
        index = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                converted = property.From(self.Language, self.Database, f"queryresult['{property.Name}']")
                # if db.UsesNamedParameters(self.Language):
                #     converted = property.From(self.Language, self.Database, f"queryresult['{property.Name}']")
                # else:
                #     converted = property.From(self.Language, self.Database, f"queryresult[{str(index)}]")
                #     index = index + 1
                s.wln(f"{property.Name.lower()} = {converted},")
        for propertyid, property in self.Class.Properties.Data.items():
            converted = property.From(self.Language, self.Database, f"queryresult['{property.Name}']")
            # if db.UsesNamedParameters(self.Language):
            #     converted = property.From(self.Language, self.Database, f"queryresult['{property.Name}']")
            # else:
            #     converted = property.From(self.Language, self.Database, f"queryresult[{str(index)}]")
            #     index = index + 1
            s.wln(f"{property.Name.lower()} = {converted},")
        s.c().wln(")")
        s.wln(f"return {self.Class.Name.lower()}")
        s.c()
        s.ret()

        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()
            s.wln("@staticmethod")
            s.wln(f'def GetSelectSingle{self.Class.Name}By{pk.Name}Query(innerquery: str="{tablename}"{iid2}):').o()
            s = self.writeInstanceStr(s)
            s.wln(f"columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()")
            s.wln(f'selectquery = f"SELECT {{columns}} FROM {{innerquery}} WHERE {db.OB()}{pk.Name}{db.CB()} = {db.GetParameter(pk.Name.lower())}{db.EndQuery()}"')
            s.wln("return selectquery")
            s.c().ret()

            s.wln("@staticmethod")
            s.wln(f'def SelectSingle{self.Class.Name}By{pk.Name}(config, {pk.Name.lower()}, innerquery: str="{tablename}"{iid2}) -> {self.Class.Name}:').o()
            if db.UsesNamedParameters(self.Language):
                s.wln(f"params = {{ '{pk.Name.lower()}': {pk.Name.lower()} }}")
            else:
                s.wln(f"params = [ {pk.Name.lower()} ]")
            s.wln(f"selectquery = {self.getDLClassName()}.GetSelectSingle{self.Class.Name}By{pk.Name}Query(innerquery{iin2})")
            #s.wln(f"result = {self.CommonFunctionsClassName}.ExecuteFetchOne(config, selectquery, params)")
            #s.wln(f"{self.Class.Name.lower()} = {self.getDLClassName()}.Get{self.Class.Name}FromQueryResult(result)")
            s.wln(f"translation = {self.getDLClassName()}.Get{self.Class.Name}FromQueryResult")
            s.wln(f"{self.Class.Name.lower()} = {self.CommonFunctionsClassName}.ExecuteFetchOne(config, selectquery, params, translation)")
            s.wln(f"return {self.Class.Name.lower()}")
            s.c()
            s.ret()

        return s
    
    def writeSelectWhere(self, s:PythonStringWriter):

        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        orderby = self.getOrderByClause()
        s.wln("@staticmethod")
        s.wln(f'def GetSelectAll{self.Class.Name}WhereQuery(whereclause: str="WHERE 1=1", limit: int = {str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}):').o()
        s.wln(f"columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()")
        s = self.writeInstanceStr(s)
        s.wln(f'selectquery = f"SELECT {db.TOP("{limit}")}{{columns}} FROM {{innerquery}} {{whereclause}}{orderby}{db.LIMIT("{limit}")}{db.EndQuery()}"')
        s.wln("return selectquery")
        s.c().ret()


        s.wln("@staticmethod")
        s.wln(f'def SelectAll{self.Class.Name}Where(config, whereclause: str="WHERE 1=1", limit: int = {str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            s.wln(f"params = {{ }}")
        else:  
            s.wln(f"params = []")
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}WhereQuery(whereclause, limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
                    s = self.writeSelectWhereForProperty(s, property)

        for propertyid, property in self.Class.Properties.Data.items(): 
            if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
                s = self.writeSelectWhereForProperty(s, property)

        return s
    
    def writeSelectWhereForProperty(self, s:PythonStringWriter, property):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()

        s.wln("@staticmethod")
        s.wln(f'def SelectAll{self.Class.Name}Where{property.Name}Like(config, val: str, limit: int = {str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            s.wln(f"params = {{ '{property.Name.lower()}': '%' + val + '%'}}")
        else:  
            s.wln(f"params = ['%' + val + '%']")
        s.wln(f'whereclause = "WHERE {db.OB()}{property.Name}{db.CB()} LIKE {db.GetParameter(property.Name.lower())}"')
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}WhereQuery(whereclause, limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()
        return s

    
    def writeSelectAll(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        orderby = self.getOrderByClause()
        s.wln("@staticmethod")
        s.wln(f'def GetSelectAll{self.Class.Name}Query(limit: int = {str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}):').o()
        s.wln(f"columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()")
        s = self.writeInstanceStr(s)
        s.wln(f'selectquery = f"SELECT {db.TOP("{limit}")}{{columns}} FROM {{innerquery}}{orderby}{db.LIMIT("{limit}")}{db.EndQuery()}"')
        s.wln("return selectquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f'def SelectAll{self.Class.Name}(config, limit: int = {str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            s.wln(f"params = {{ }}")
        else:  
            s.wln(f"params = []")
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}Query(limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()

        s.wln("@staticmethod")
        s.wln(f"def Select{self.Class.SetDescription}(config, selectquery, params) -> {self.Class.SetDescription}:").o()
        s.wln(f"translation = {self.getDLClassName()}.Get{self.Class.Name}FromQueryResult")
        s.wln(f"_{self.Class.Name.lower()}_list = {self.CommonFunctionsClassName}.ExecuteFetchAll(config, selectquery, params, translation)")
        s.wln(f"{self.Class.Name.lower()}_list = {self.Class.SetDescription}().fromList(_{self.Class.Name.lower()}_list)")
        s.wln(f"return {self.Class.Name.lower()}_list")
        s.c()
        s.ret()
        return s
    
    def getOrderByClause(self):
        db = self.Database
        orderby = ""
        # if self.Class.hasPrimaryKeyPoperty():
        #     pk = self.Class.getPrimaryKeyProperty()
        #     orderby = f" ORDER BY {db.OB()}{pk.Name}{db.CB()} ASC"

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                if property.IsUnique and not property.IsPrimaryKey:
                    orderby = f" ORDER BY {db.OB()}{property.Name}{db.CB()} ASC"
        for propertyid, property in self.Class.Properties.Data.items():
            if property.IsUnique and not property.IsPrimaryKey:
                    orderby = f" ORDER BY {db.OB()}{property.Name}{db.CB()} ASC"
        return orderby
    
    def writeSelectPage(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        orderby = self.getOrderByClause()
        s.wln("@staticmethod")
        s.wln(f'def GetSelectPaged{self.Class.Name}Query(pageno: int=1, limit: int={str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}):').o()
        s.wln(f"offset = (pageno - 1) * limit")
        s.wln(f"columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()")
        s = self.writeInstanceStr(s)
        s.wln(f'selectquery = f"SELECT {{columns}} FROM {{innerquery}}{orderby}{db.LIMIT_OFFSET("{limit}","{offset}")}{db.EndQuery()}"')
        s.wln("return selectquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f'def SelectPaged{self.Class.Name}(config, pageno: int=1, limit: int={str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            #s.wln(f"params = {{ 'pageno': pageno, 'limit': limit }}")
            s.wln(f"params = {{ }}")
        else:
            #s.wln(f"params = [ pageno, limit ]")
            s.wln(f"params = []")
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectPaged{self.Class.Name}Query(pageno, limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()
        return s
    
    def writeSelectPageWhere(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        orderby = self.getOrderByClause()
        s.wln("@staticmethod")
        s.wln(f'def GetSelectPaged{self.Class.Name}WhereQuery(whereclause: str="WHERE 1=1", pageno: int=1, limit: int={str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}):').o()
        s.wln(f"offset = (pageno - 1) * limit")
        s.wln(f"columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames()")
        s = self.writeInstanceStr(s)
        s.wln(f'selectquery = f"SELECT {{columns}} FROM {{innerquery}} {{whereclause}}{orderby}{db.LIMIT_OFFSET("{limit}","{offset}")}{db.EndQuery()}"')
        s.wln("return selectquery")
        s.c().ret()

        s.wln("@staticmethod")
        s.wln(f'def SelectPaged{self.Class.Name}Where(config, whereclause: str="WHERE 1=1", pageno: int=1, limit: int={str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            #s.wln(f"params = {{ 'pageno': pageno, 'limit': limit }}")
            s.wln(f"params = {{ }}")
        else:
            #s.wln(f"params = [ pageno, limit ]")
            s.wln(f"params = []")
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectPaged{self.Class.Name}WhereQuery(whereclause, pageno, limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
                    s = self.writeSelectPagedWhereForProperty(s, property)

        for propertyid, property in self.Class.Properties.Data.items(): 
            if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
                s = self.writeSelectPagedWhereForProperty(s, property)

        return s
    
    def writeFilterPage(self, s:PythonStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()
        s.wln("@staticmethod")
        s.wln(f'def FilterPaged{self.Class.Name}(config, {self.Class.Name.lower()}filter: list, pageno: int=1, limit: int={str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            #s.wln(f"params = {{ 'pageno': pageno, 'limit': limit }}")
            s.wln(f"params = {{ }}")
        else:
            #s.wln(f"params = [ pageno, limit ]")
            s.wln(f"params = []")
        s.wln(f'whereclause = "WHERE 1=1"')
        s.wln(f"for filteritem in {self.Class.Name.lower()}filter:").o()
        s.wln(f'whereclause += f" AND {db.OB()}{{filteritem.PropertyName}}{db.CB()} {{filteritem.Comparator}} {{filteritem.CompareTo}}"')
        s.c()
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectPaged{self.Class.Name}WhereQuery(whereclause, pageno, limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()
        return s


    def writeSelectPagedWhereForProperty(self, s:PythonStringWriter, property):
        (db, schema, tablename, iid, iid2, iin, iin2) = self.getCommonItems()

        s.wln("@staticmethod")
        s.wln(f'def SelectPaged{self.Class.Name}Where{property.Name}Like(config, val: str, pageno: int=1, limit: int={str(self.Class.PageSize)}, innerquery: str="{tablename}"{iid2}) -> {self.Class.SetDescription}:').o()
        if db.UsesNamedParameters(self.Language):
            s.wln(f"params = {{ '{property.Name.lower()}': '%' + val + '%'}}")
        else:  
            s.wln(f"params = ['%' + val + '%']")
        s.wln(f'whereclause = "WHERE {db.OB()}{property.Name}{db.CB()} LIKE {db.GetParameter(property.Name.lower())}"')
        s.wln(f"selectquery = {self.getDLClassName()}.GetSelectPaged{self.Class.Name}WhereQuery(whereclause, pageno, limit, innerquery{iin2})")
        s.wln(f"result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, params)")
        s.wln(f"return result")
        s.c()
        s.ret()
        return s

    def writeDLClassClose(self, s:PythonStringWriter):
        s.c()
        return s
