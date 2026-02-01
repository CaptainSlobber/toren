import collections
import json
import os
from pathlib import Path

from typing import List
from ..DataClassWriter import DataClassWriter
from .JavaStringWriter import JavaStringWriter
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class JavaDataClassWriter(DataClassWriter):

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
        self.StringWriterClass = JavaStringWriter
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
        for dependency in self.Database.JavaDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name.lower()
        b = self.Module.Name.lower()
        t = self.Class.ParentModule.ParentProject.TLD.lower()
        object_import = f"import {t}.{e}.{p}.{m}.{self.Class.Name};"
        
        uuiddep = "import java.util.UUID;"
        listdep = "import java.util.ArrayList;"
        arrlistdep = "import java.util.List;"
        if self.Class.Cloneable: 
            dependency_map[uuiddep] = uuiddep
        dependency_map[listdep] = listdep
        dependency_map[arrlistdep] = arrlistdep
        dependency_map[object_import] = object_import
        return dependency_map
    
    def writeDLPackage(self, s:JavaStringWriter):
        p = self.Class.ParentModule.ParentProject.Name.lower()
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name.lower()
        b = self.Database.Name.lower()
        t = self.Class.ParentModule.ParentProject.TLD.lower()
        s.wln(f"package {t}.{e}.{p}.{m}.{b};")
        s.ret()
        return s
    
    def getDataModulePath(self):
        return self.getParentModulePath()

    def getParentModulePath(self):
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD.lower()
        src = "src"
        main = "main"
        java = "java"
        dbmod = f"{m}.{b}"

        data_module_path = os.path.join(self.Language.OutputDirectory,p, dbmod, src, main, java, t, e, p, m, b)
        return data_module_path

    def writeDLClassOpen(self, s:JavaStringWriter):

        
        c = self.Class.Name
        d = self.getDLClassName()
        
        s.ret()
        s.write(f"public class {d} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" {self.Database.Name} Data Layer for Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("*/")
        s.ret()
        return s
    
    def writeParentClassInitializer(self, s:JavaStringWriter):
        return s

    def writeDLClassInitializer(self, s:JavaStringWriter):
        #d = self.getDLClassName()
        #s.wln(f"public {d}() {{}}")
        #s.ret()
        return s
    
    def writeDLClassProperties(self, s:JavaStringWriter):
        s.wln(f"public static String SCHEMA_NAME = \"{self.Class.ParentModule.Name}\";")
        s.wln(f"public static String TABLE_NAME = \"{self.Class.Name}\";")
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s.wln(f"public static String COL_NAME_{property.Name.upper()} = \"{property.Name}\";")
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"public static String COL_NAME_{property.Name.upper()} = \"{property.Name}\";")
        s.ret()
        return s
    

    def writeCreateTableColumn(self, s:JavaStringWriter, property):
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
        
        s.wln(f'createquery += "{db.OB()}{property.Name}{db.CB()} {DATATYPE}{NOTNULL}{UNIQUE}{PRIMARYKEY},";')
        return s


    def getInstanceIDParameter(self, prefix: str = ""):
        if self.Class.Cloneable:
            return prefix + "UUID " + self.getInstanceIDParemeterName() + ""
        else:
            return ""
    
    def  getInstanceIDParemeterName(self, prefix: str = ""):
        if self.Class.Cloneable:
            return prefix + "instanceID"
        else:
            return ""
        
    def getInstanceIDExt(self):
        if self.Class.Cloneable:
            return "" + self.getInstanceIDParemeterName() + "Str" + ""

        else:
            return ""

    def writeGetTableName(self, s:JavaStringWriter):
        
        iin = self.getInstanceIDParemeterName("")
        if self.Class.Cloneable:
            s.wln(f"String tableName = {self.getDLClassName()}.GetTableName({iin});")
        else:
            s.wln(f"String tableName = {self.getDLClassName()}.GetTableName();")
        return s
    
    def getCommonItems(self):
        db = self.Database
        iin = self.getInstanceIDParemeterName()
        iin2 = self.getInstanceIDParemeterName(", ")

        iid = self.getInstanceIDParameter()
        iid2 = self.getInstanceIDParameter(", ")
        schema = self.getSchema()
        tablename = db.GetTableName(self.Class)
        conobjclass = f"{self.ConnectionObjectClassName}"
        return (db, schema, tablename, iid, iid2, iin, iin2, conobjclass)

    def writeCreateTable(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        
        if self.Class.Cloneable:
            s.w(f'private static String GetTableName({iid}) ').o()
            s.wln(f"String id = {iin}.toString();")
            s.wln(f'String tableName = String.format("{db.GetTableName(self.Class, ".%s")}", id);')     
            s.wln(f'return tableName;')
            s.c()
            s.ret()
        else:
            s.w(f'private static String GetTableName() ').o()
            s.wln(f'String tableName = "{db.GetTableName(self.Class)}";')
            s.wln(f'return tableName;')
            s.c()
            s.ret()


        s.w(f"private static String GetCreate{self.Class.Name}TableQuery ({iid})").o()
        s = self.writeGetTableName(s)
        s.wln(f'String createquery = String.format("CREATE TABLE{db.IfNotExists()} %s (", tableName);')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s = self.writeCreateTableColumn(s, property)
        for propertyid, property in self.Class.Properties.Data.items():
            s = self.writeCreateTableColumn(s, property)
        s.wln(f'createquery += "){db.EndQuery()}";')
        s.wln("return createquery;")
        s.c().ret()

        s.w(f"public static void Create{self.Class.Name}Table ({conobjclass} config{iid2}) ").o()
        s.wln(f'String createquery = {self.getDLClassName()}.GetCreate{self.Class.Name}TableQuery({iin});')
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, createquery);")
        s.c()
        s.ret()
        return s
    

    def writeClearTable(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        s.w(f"private static String GetClear{self.Class.Name}TableQuery({iid}) ").o()
        s = self.writeGetTableName(s)
        s.wln(f'String clearquery = String.format("DELETE FROM %s{db.EndQuery()}", tableName);')
        s.wln("return clearquery;")
        s.c()
        s.ret()

        s.w(f"public static void Clear{self.Class.Name}Table({conobjclass} config{iid2}) ").o()
        s.wln(f"String clearquery = {self.getDLClassName()}.GetClear{self.Class.Name}TableQuery({iin});")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, clearquery);")
        s.c()
        s.ret()
        return s
    
    def writeDropTable(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        s.w(f"private static String GetDrop{self.Class.Name}TableQuery({iid}) ").o()
        s = self.writeGetTableName(s)
        s.wln(f'String dropquery = String.format("DROP TABLE{db.IfExists()} %s{db.EndQuery()}", tableName);')
        s.wln("return dropquery;")
        s.c()
        s.ret()

        s.w(f"public static void Drop{self.Class.Name}Table({conobjclass} config{iid2}) ").o()
        s.wln(f"String dropquery = {self.getDLClassName()}.GetDrop{self.Class.Name}TableQuery({iin});")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, dropquery);")
        s.c()
        s.ret()
        return s

    

    def writeGetColumnNames(self, s:JavaStringWriter):
        db = self.Database
        columns = []
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        for propertyid, property in self.Class.Properties.Data.items():
            columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        columns_string = ", ".join(columns)
        s.w(f"private static String Get{self.Class.Name}ColumnNames() ").o()
        s.wln(f'String columns = "{columns_string}";')
        s.wln("return columns;")
        s.c()
        s.ret()
        return s
    
    def writeGetColumnParameters(self, s:JavaStringWriter):
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
        s.w(f"private static String Get{self.Class.Name}ColumnParameters() ").o()
        s.wln(f'String params = "{params_string}";')
        s.wln("return params;")
        s.c()
        s.ret()
        return s
    
    def writeCreateForeignKeys(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        if db.SeparateForeignKeyCreation():
            s.w(f"private static List<String> Get{self.Class.Name}ForeignKeyQueries({iid}) ").o()
            s = self.writeGetTableName(s)

            s.wln("List<String> foreignkeyqueries = new ArrayList<>();")
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if property.ForeignKey is not None:
                        create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "%s")
                        s.wln(f'foreignkeyqueries.add(String.format("{create_fk}", tableName));')
                        

            for propertyid, property in self.Class.Properties.Data.items():
                if property.ForeignKey is not None:
                    create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "%s")
                    s.wln(f'foreignkeyqueries.add(String.format("{create_fk}", tableName));')
            s.writeline("return foreignkeyqueries;")
            s.c()
            s.ret()

            s.w(f"public static void Create{self.Class.Name}ForeignKeys({conobjclass} config{iid2}) ").o()
            s.wln(f"List<String> foreignkeyqueries = {self.getDLClassName()}.Get{self.Class.Name}ForeignKeyQueries({iin});")
            s.w(f"for (String foreignkeyquery: foreignkeyqueries) ").o()
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, foreignkeyquery);")
            s.c()
            s.c()
            s.ret()
        return s

    def writeInsertItem(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()

        s.w(f"private static String Get{self.Class.Name}InsertQuery({iid}) ").o()
        s = self.writeGetTableName(s)
        s.wln(f'String columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames();')
        s.wln(f"String params = {self.getDLClassName()}.Get{self.Class.Name}ColumnParameters();")
        s.wln(f'String insertquery = String.format("INSERT INTO %s (%s) VALUES (%s){db.EndQuery()}", tableName, columns, params);')
        s.wln("return insertquery;")
        s.c().ret()


        s.w(f"public static void InsertSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2}) ").o()
        #s.wln(f"params = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()})")

        s.wln(f"Connection connection = {self.CommonFunctionsClassName}.GetConnection(config);")
        s.wln(f"String insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin});")

        s.w("try ").o()
        s.wln("PreparedStatement statement = connection.prepareStatement(insertquery);")
        s.wln(f'statement = {self.getDLClassName()}.Prepare{self.Class.Name}Statement(statement, {self.Class.Name.lower()});')
        s = self.writeCommonCleanupConnection(s)
        #s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, insertquery, params)")
        s.c()
        s.ret()


        s.w(f"private static PreparedStatement Prepare{self.Class.Name}Statement(PreparedStatement statement, {self.Class.Name} {self.Class.Name.lower()})").o()
        
        n = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                n = n + 1
                s.wln(f'statement.setString({n}, {self.Class.Name.lower()}.get{property.Name}());')
        for propertyid, property in self.Class.Properties.Data.items():
            n = n + 1
            s.wln(f'statement.setString({n}, {self.Class.Name.lower()}.get{property.Name}());')
        s.wln("return statement;")
        s.c()
        s.ret()
        return s
    

    def writeCommonCleanupConnection(self, s:JavaStringWriter):
        cfn = self.CommonFunctionsClassName
        #s.w("try ").o()
        s.wln(f"connection.close();")
        s.b(" catch (SQLException e) ")
        s.wln(f"{cfn}.HandleSQLException(e);")
        s.c()
        return s
    
    def writeInsertCollection(self, s:JavaStringWriter):
        return s
    
    def writeUpdate(self, s:JavaStringWriter):
        return s
    
    def writeDelete(self, s:JavaStringWriter):
        return s
    
    def writeSelectSingleRecordByPK(self, s:JavaStringWriter):
        return s
    
    def writeSelectWhere(self, s:JavaStringWriter):
        return s

    def writeDLClassClose(self, s:JavaStringWriter):
        s.c()
        return s