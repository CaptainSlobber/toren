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

        for propertyid, property in self.Class.Properties.Data.items():
            for dependency in property.Java_Dependencies():
                if dependency not in dependency_map:
                    dependency_map[dependency] = dependency

        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                for dependency in property.Java_Dependencies():
                    if dependency not in dependency_map:
                        dependency_map[dependency] = dependency

        for dependency in self.Database.JavaDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        e = self.Class.ParentModule.ParentProject.Entity.lower()
        m = self.Class.ParentModule.Name.lower()
        b = self.Module.Name.lower()
        t = self.Class.ParentModule.ParentProject.TLD.lower()
        object_import = f"import {t}.{e}.{p}.{m}.{self.Class.Name};"
        object_set_import = f"import {t}.{e}.{p}.{m}.{self.Class.SetDescription};"
        
        uuiddep = "import java.util.UUID;"
        listdep = "import java.util.ArrayList;"
        arrlistdep = "import java.util.List;"
        lhmdep = "import java.util.LinkedHashMap;"
        hmdep = "import java.util.Map;"
        gsondep = "import com.google.gson.Gson;"
        charsetsdep = "import java.nio.charset.StandardCharsets;"
        if self.Class.Cloneable: 
            dependency_map[uuiddep] = uuiddep
        dependency_map[listdep] = listdep
        dependency_map[arrlistdep] = arrlistdep
        dependency_map[hmdep] = hmdep
        dependency_map[lhmdep] = lhmdep
        if self.hasHigherDimensionalProperty():
            dependency_map[gsondep] = gsondep
            dependency_map[charsetsdep] = charsetsdep
        



        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                for dependency in property.Java_Datalayer_Dependencies():
                    dependency_map[dependency] = dependency
        for propertyid, property in self.Class.Properties.Data.items():
            for dependency in property.Java_Datalayer_Dependencies():
                dependency_map[dependency] = dependency

        dependency_map[object_import] = object_import
        dependency_map[object_set_import] = object_set_import       
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

    def writeInstanceStr(self, s:JavaStringWriter, iq:str ="innerquery", initializevar:bool=True):
        iin2 = self.getInstanceIDParemeterName(", ")

        strstr = ""
        if (initializevar):
            strstr = "String "
        if self.Class.Cloneable:
            s.wln(f"{strstr}innerquery = {self.getDLClassName()}.GetInnerQuery({iq}{iin2});")
        else:
            s.wln(f"{strstr}innerquery = {self.getDLClassName()}.GetInnerQuery({iq});")
        return s


    def writeGetTableName(self, s:JavaStringWriter):
        
        iin = self.getInstanceIDParemeterName("")
        if self.Class.Cloneable:
            s.wln(f"String tableName = {self.getDLClassName()}.GetInnerQuery({iin});")
        else:
            s.wln(f"String tableName = {self.getDLClassName()}.GetInnerQuery();")
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
        tablename = db.GetTableName(self.Class)
        if self.Class.Cloneable:
            s.w(f'private static String GetInnerQuery({iid}) ').o()
            s.wln(f"String id = {iin}.toString();")
            s.wln(f'String tableName = String.format("{db.GetTableName(self.Class, ".%s")}", id);')     
            s.wln(f'return tableName;')
            s.c()
            s.ret()

            s.w(f'private static String GetInnerQuery(String innerquery{iid2}) ').o()   
            s.wln(f'return innerquery;')
            s.c()
            s.ret()
        else:
            s.w(f'private static String GetInnerQuery() ').o()
            s.wln(f'String tableName = "{db.GetTableName(self.Class)}";')
            s.wln(f'return tableName;')
            s.c()
            s.ret()

            s.w(f'private static String GetInnerQuery(String innerquery) ').o()
            s.wln(f'String tableName = "{db.GetTableName(self.Class)}";')
            s.w(f'if (innerquery==null)').o()
            s.wln('innerquery = tableName;')
            s.c()
            s.wln(f'return innerquery;')
            s.c()
            s.ret()


        s.w(f"private static String GetCreate{self.Class.Name}TableQuery({iid}) ").o()
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

        s.w(f"public static void Create{self.Class.Name}Table({conobjclass} config{iid2}) ").o()
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
        n = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                if not property.IsPrimaryKey:
                    n = n + 1
                    columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        for propertyid, property in self.Class.Properties.Data.items():
            if not property.IsPrimaryKey:
                n = n + 1
                columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        n = n + 1
        pk = self.Class.getPrimaryKeyProperty()
        columns.append(f"{db.OB()}{pk.Name}{db.CB()}")
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
                if not property.IsPrimaryKey:
                    n = n + 1
                    params.append(f"{db.GetParameter(self.Language, property.Name.lower(), n)}")
        for propertyid, property in self.Class.Properties.Data.items():
            if not property.IsPrimaryKey:
                n = n + 1
                params.append(f"{db.GetParameter(self.Language, property.Name.lower(), n)}")
        n = n + 1
        pk = self.Class.getPrimaryKeyProperty()
        params.append(f"{db.GetParameter(self.Language, pk.Name.lower(), n)}")
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

        s.w(f"public static int InsertSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2}) ").o()
        s.wln(f"Connection connection = {self.CommonFunctionsClassName}.GetConnection(config);")
        s.wln(f"String insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin});")
        s.wln(f"PreparedStatement statement = {self.getDLClassName()}.GetPreparedStatementFrom{self.Class.Name}(connection, {self.Class.Name.lower()}, insertquery);")
        s.wln(f"int affectedRows = {self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(connection, statement);")
        s.wln("return affectedRows;")
        s.c()
        s.ret()
        return s
    
    def writeCloseTry(self, s:JavaStringWriter):
        cfn = self.CommonFunctionsClassName
        s.b(" catch (SQLException e) ")
        s.wln(f"{cfn}.HandleSQLException(e);")
        s.c()
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
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
    
        s.w(f"public static int Insert{self.Class.SetDescription}({conobjclass} config, {self.Class.SetDescription} {self.Class.SetDescription.lower()}{iid2}) ").o()
        s.wln(f"ArrayList<{self.Class.Name}> {self.Class.Name.lower()}list = {self.Class.SetDescription.lower()}.toList();")
        s.wln(f"return {self.getDLClassName()}.Insert{self.Class.Name}List(config, {self.Class.Name.lower()}list{iin2});")
        s.c()
        s.ret()
            
        s.w(f"public static int Insert{self.Class.Name}List({conobjclass} config, ArrayList<{self.Class.Name}> {self.Class.Name.lower()}list{iid2}) ").o()
        s.wln(f"int affectedRows = 0;")
        s.w(f"for (int i=0; i<{self.Class.Name.lower()}list.size(); i++)").o()
        s.wln(f"{self.Class.Name} {self.Class.Name.lower()} = {self.Class.Name.lower()}list.get(i);")
        s.wln(f"affectedRows += {self.getDLClassName()}.InsertSingle{self.Class.Name}(config, {self.Class.Name.lower()}{iin2});")
        s.c()
        s.wln("return affectedRows;")
        s.c()
        s.ret()
        return s
        
    
    def writeUpdate(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()
            s.w(f"public static String Get{self.Class.Name}UpdateQuery({iid}) ").o()
            s.wln(f'String whereclause = " WHERE {db.OB()}{pk.Name}{db.CB()} = {db.GetParameter(self.Language, pk.Name.lower())}{db.EndQuery()}";')
            s = self.writeGetTableName(s)
            s.wln(f'String updatequery = String.format("UPDATE %s SET ", tableName);')
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if not property.IsPrimaryKey:
                        s.wln(f'updatequery += "{db.OB()}{property.Name}{db.CB()} = {db.GetParameter(self.Language, property.Name.lower())},";')
            for propertyid, property in self.Class.Properties.Data.items():
                if not property.IsPrimaryKey:
                    s.wln(f'updatequery += "{db.OB()}{property.Name}{db.CB()} = {db.GetParameter(self.Language, property.Name.lower())},";')
            s.wln(f'updatequery = updatequery.substring(0, updatequery.length() - 1) + " " + whereclause;')
            s.wln("return updatequery;")
            s.c().ret()


            s.w(f"public static PreparedStatement GetPreparedStatementFrom{self.Class.Name}(Connection connection, {self.Class.Name} {self.Class.Name.lower()}, String query) ").o()
            s.wln("PreparedStatement statement = null;")
            s.w("try ").o()
            s.wln("statement = connection.prepareStatement(query);")
            if self.hasHigherDimensionalProperty():
                s.wln("Gson gson = new Gson();")
            n = 0
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if not property.IsPrimaryKey:
                        n = n + 1
                        setval = property.To(self.Language, self.Database, n, self.Class.Name.lower(), property.Name)
                        s.wln(f'{setval}')
            for propertyid, property in self.Class.Properties.Data.items():
                if not property.IsPrimaryKey:
                    n = n + 1
                    setval = property.To(self.Language, self.Database, n, self.Class.Name.lower(), property.Name)
                    s.wln(f'{setval}')
            n = n + 1
            setpkval = pk.To(self.Language, self.Database, n, self.Class.Name.lower(), pk.Name)
            s.wln(f'{setpkval}')
            s = self.writeCloseTry(s)
            s.wln("return statement;")
            s.c()
            s.ret()



            s.w(f"public static int UpdateSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2}) ").o()

            s.wln(f"Connection connection = {self.CommonFunctionsClassName}.GetConnection(config);")
            s.wln(f"String updatequery = {self.getDLClassName()}.Get{self.Class.Name}UpdateQuery({iin});")
            s.wln(f"PreparedStatement statement = {self.getDLClassName()}.GetPreparedStatementFrom{self.Class.Name}(connection, {self.Class.Name.lower()}, updatequery);")
            s.wln(f"int affectedRows = {self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(connection, statement);")
            s.wln("return affectedRows;")
            s.c()
            s.ret()
        return s


    def writePersistRecord(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()

            s.w(f"public static {pk.PropertyType(self.Language)} PersistSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2}) ").o()
            
            s.wln(f"Connection connection = {self.CommonFunctionsClassName}.GetConnection(config);")
            s.wln(f"{pk.PropertyType(self.Language)} _{pk.Name.lower()} = {self.Class.Name.lower()}.get{pk.Name}();")
            s.wln(f'String whereclause = String.format("WHERE {db.OB()}{pk.Name}{db.CB()} = \'%s\'", _{pk.Name.lower()});')
            s.wln(f"{self.Class.SetDescription} {self.Class.Name.lower()}_items = {self.getDLClassName()}.SelectAll{self.Class.Name}Where(config, whereclause);")
            s.w(f"if ({self.Class.Name.lower()}_items.count() == 1)").o()

            s.wln(f"String updatequery = {self.getDLClassName()}.Get{self.Class.Name}UpdateQuery({iin});")
            s.wln(f"PreparedStatement statement = {self.getDLClassName()}.GetPreparedStatementFrom{self.Class.Name}(connection, {self.Class.Name.lower()}, updatequery);")
            s.wln(f"int affectedRows = {self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(connection, statement);")
            s.wln(f"_{pk.Name.lower()} = ({pk.PropertyType(self.Language)}) {self.Class.Name.lower()}_items.toArray()[0].get{pk.Name}();")
            s.b("else")
            
            s.wln(f"String insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin});")
            s.wln(f"PreparedStatement statement = {self.getDLClassName()}.GetPreparedStatementFrom{self.Class.Name}(connection, {self.Class.Name.lower()}, insertquery);")
            s.wln(f"int affectedRows = {self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(connection, statement);")
            s.c()
            s.wln(f"return _{pk.Name.lower()};");
            s.c()
            s.ret()
            # if self.Class.InheritsFrom is not None:
            #     for propertyid, property in self.Class.InheritedProperties.Data.items():
            #         if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
            #             s = self.writePersistWhereForProperty(s, property, pk)

            # for propertyid, property in self.Class.Properties.Data.items(): 
            #     if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
            #         s = self.writePersistWhereForProperty(s, property, pk)
        return s


    def writeSelectAll(self, s:JavaStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        orderby = self.getOrderByClause()

        s.w(f'private static String GetSelectAll{self.Class.Name}Query(int limit, String innerquery{iid2}) ').o()
        #limit={str(self.Class.PageSize)}
        s = self.writeInstanceStr(s, initializevar=False)
        s.wln(f"String columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames();")

        s.wln(f'String topstring = String.format("{db.TOP("%d")}", limit);')
        s.wln(f'String limitstring = String.format("{db.LIMIT("%d")}", limit);')
        s.wln(f'String selectquery = String.format("SELECT %s%s FROM %s{orderby}%s{db.EndQuery()}", topstring, columns, innerquery, limitstring);')
        s.wln("return selectquery;")
        s.c().ret()


        s.w(f'public static {self.Class.SetDescription} SelectAll{self.Class.Name}({conobjclass} config, int limit, String innerquery{iid2}) ').o()
        s = self.writeInstanceStr(s, initializevar=False)
        s.wln(f"String selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}Query(limit, innerquery{iin2});")
        s.wln(f"Connection connection = {self.CommonFunctionsClassName}.GetConnection(config);")
        s.wln(f"Map<String, Map<String, Object>> parameters = new LinkedHashMap<>();")
        s.wln(f"PreparedStatement statement = {self.CommonFunctionsClassName}.PrepareStatement(connection, selectquery, parameters);")
        s.wln(f"{self.Class.SetDescription} result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, statement);")
        s.wln(f"return result;")
        s.c()
        s.ret()


        s.w(f"public static {self.Class.SetDescription} Select{self.Class.SetDescription}({conobjclass} config, PreparedStatement statement) ").o()
        # s.wln(f"Func<{readerclass}, object> translation = {self.getDLClassName()}.Get{self.Class.Name}FromQueryResult;")
        # s.wln(f"List<{self.Class.Name}> _{self.Class.Name.lower()}_list = {self.CommonFunctionsClassName}.ExecuteFetchAll(config, selectquery, parameters, translation).Cast<{self.Class.Name}>().ToList();;")
        # s.wln(f"{self.Class.SetDescription} {self.Class.Name.lower()}_list = new {self.Class.SetDescription}().fromList(_{self.Class.Name.lower()}_list);")


        s.wln(f"List<{self.Class.Name}> _{self.Class.Name.lower()}_list = new ArrayList<{self.Class.Name}>();")

        s.wln(f"return {self.Class.Name.lower()}_list;")
        s.c()
        s.ret()
        return s

    def writeParameterMapKeys(self, s:JavaStringWriter):
        s.wln("String param_value_key = \"Value\";")
        s.wln("String param_dbtype_key = \"DbType\";")
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