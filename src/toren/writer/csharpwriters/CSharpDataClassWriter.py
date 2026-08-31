import collections
import json
import os
from pathlib import Path

from typing import List

from ..DataClassWriter import DataClassWriter
from .CSharpStringWriter import CSharpStringWriter
from ...datatypes import *
from ...datastores.Database import Database
from ...Project import Project
from ...Module import Module
from ...Class import Class
from ...languages import *
from ...tracer.Logger import Logger

class CSharpDataClassWriter(DataClassWriter):

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
        self.StringWriterClass = CSharpStringWriter
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
        for dependency in self.Database.CSharpDependencies():
            dependency_map[dependency] = dependency
        p = self.Class.ParentModule.ParentProject.Name
        m = self.Class.ParentModule.Name
        c = self.Class.Name
        textdep = "using System.Text;"
        dependency_map[textdep] = textdep
        #jsondep = "using System.Text.Json;"
        jsondep = "using Newtonsoft.Json;"
        dependency_map[jsondep] = jsondep

        
        return dependency_map
    

    def getDataModulePath(self) -> str:
        p = self.Module.ParentProject.Name.lower()
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name.lower()
        t = self.Module.ParentProject.TLD.lower()

        dbmod = f"{e.lower()}.{p.lower()}.{self.Module.Name.lower()}.{self.Database.Name.lower()}"
        data_module_path = os.path.join(self.Language.OutputDirectory, 
                                                self.Project.Name, 
                                                dbmod)
        return data_module_path


    def writeDLPackage(self, s:CSharpStringWriter):
        p = self.Module.ParentProject.Name
        e = self.Module.ParentProject.Entity.lower()
        m = self.Module.Name
        b = self.Database.Name.lower()
        t = self.Module.ParentProject.TLD
        s.wln(f"namespace {e}.{p}.{m}.{b};")
        s.ret()
        return s


    def writeDLClassOpen(self, s:CSharpStringWriter):

        
        c = self.Class.Name
        d = self.getDLClassName()
        
        s.ret()
        s.write(f"public static class {d} ").o()
        s.ret()
        s.wln("/*")
        s.wln(f" {self.Database.Name} Data Layer for Class: {self.Class.Name}")
        s.wln(f" Class ID: {self.Class.ID}")
        s.wln("*/")
        s.ret()
        return s


    def writeParentClassInitializer(self, s:CSharpStringWriter):
        return s

    def writeDLClassInitializer(self, s:CSharpStringWriter):
        #d = self.getDLClassName()
        #s.wln(f"public {d}() {{}}")
        #s.ret()
        return s

    def writeDLClassClose(self, s:CSharpStringWriter):
        s.c()
        return s

    def writeDLClassProperties(self, s:CSharpStringWriter):
        s.wln(f"public static string SCHEMA_NAME = \"{self.Class.ParentModule.Name}\";")
        s.wln(f"public static string TABLE_NAME = \"{self.Class.Name}\";")
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s.wln(f"public static string COL_NAME_{property.Name.upper()} = \"{property.Name}\";")
        for propertyid, property in self.Class.Properties.Data.items():
            s.wln(f"public static string COL_NAME_{property.Name.upper()} = \"{property.Name}\";")
        s.ret()
        return s

    def writeCreateTableColumn(self, s:CSharpStringWriter, property):
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
            return prefix + "Guid? " + self.getInstanceIDParemeterName() + " = null"
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

    def writeInstanceStr(self, s:CSharpStringWriter, iq:str ="innerquery"):
        iin2 = self.getInstanceIDParemeterName(", ")
        if self.Class.Cloneable:
            s.wln(f"string innerquery = {self.getDLClassName()}.GetInnerQuery({iq}{iin2});")
        else:
            s.wln(f"string innerquery = {self.getDLClassName()}.GetInnerQuery({iq});")
        return s

    def writeGetTableName(self, s:CSharpStringWriter):
        
        iin = self.getInstanceIDParemeterName("")
        if self.Class.Cloneable:
            s.wln(f"string tableName = {self.getDLClassName()}.GetInnerQuery({iin});")
        else:
            s.wln(f"string tableName = {self.getDLClassName()}.GetInnerQuery();")
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

    def writeCreateTable(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        tablename = db.GetTableName(self.Class)
        if self.Class.Cloneable:

            s.w(f'private static string GetInnerQuery({iid})').o()
            #s.wln(f'string innerquery="{tablename}";')
            #s.w(f"if ({iin} != null)").o()
            s.wln(f"string id = {iin}.ToString();")
            s.wln(f'return $"{db.GetTableName(self.Class, ".{id}")}";')     
            #s.c()
            s.c()
            s.ret()

            s.w(f'private static string GetInnerQuery(string innerquery{iid2})').o()
            #s.w(f"if ({iin} != null)").o()
            #s.wln(f"string id = {iin}.ToString();")
            #s.wln(f'return $"{db.GetTableName(self.Class, ".{id}")}";')     
            #s.c()
            s.wln(f'return innerquery;')
            s.c()
            s.ret()

        else:

            s.w(f'private static string GetInnerQuery(string innerquery="{tablename}")').o()
            s.wln(f'return innerquery;')
            s.c()
            s.ret()


        s.w(f"private static string GetCreate{self.Class.Name}TableQuery({iid})").o()
        s = self.writeGetTableName(s)
        s.wln(f'string createquery = $"CREATE TABLE{db.IfNotExists()} {{tableName}} (";')
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                s = self.writeCreateTableColumn(s, property)
        for propertyid, property in self.Class.Properties.Data.items():
            s = self.writeCreateTableColumn(s, property)
        s.wln(f'createquery += "){db.EndQuery()}";')
        s.wln("return createquery;")
        s.c().ret()

        s.w(f"public static void Create{self.Class.Name}Table({conobjclass} config{iid2}) ").o()
        s.wln(f'string createquery = {self.getDLClassName()}.GetCreate{self.Class.Name}TableQuery({iin});')
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, createquery);")
        s.c()
        s.ret()
        return s

    
    def writeClearTable(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        s.w(f"private static string GetClear{self.Class.Name}TableQuery({iid}) ").o()
        s = self.writeGetTableName(s)
        s.wln(f'string clearquery = $"DELETE FROM {{tableName}}{db.EndQuery()}";')
        s.wln("return clearquery;")
        s.c()
        s.ret()

        s.w(f"public static void Clear{self.Class.Name}Table({conobjclass} config{iid2}) ").o()
        s.wln(f"string clearquery = {self.getDLClassName()}.GetClear{self.Class.Name}TableQuery({iin});")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, clearquery);")
        s.c()
        s.ret()
        return s


    def writeDropTable(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        s.w(f"private static string GetDrop{self.Class.Name}TableQuery({iid}) ").o()
        s = self.writeGetTableName(s)
        s.wln(f'string dropquery = $"DROP TABLE{db.IfExists()} {{tableName}}{db.EndQuery()}";')
        s.wln("return dropquery;")
        s.c()
        s.ret()

        s.w(f"public static void Drop{self.Class.Name}Table({conobjclass} config{iid2}) ").o()
        s.wln(f"string dropquery = {self.getDLClassName()}.GetDrop{self.Class.Name}TableQuery({iin});")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, dropquery);")
        s.c()
        s.ret()
        return s

    def writeGetColumnNames(self, s:CSharpStringWriter):
        db = self.Database
        columns = []
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        for propertyid, property in self.Class.Properties.Data.items():
            columns.append(f"{db.OB()}{property.Name}{db.CB()}")
        columns_string = ", ".join(columns)
        s.w(f"private static string Get{self.Class.Name}ColumnNames() ").o()
        s.wln(f'string columns = "{columns_string}";')
        s.wln("return columns;")
        s.c()
        s.ret()
        return s

    def writeGetColumnParameters(self, s:CSharpStringWriter):
        db = self.Database
        params = []
        n = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                n = n + 1
                params.append(f"{db.GetParameter(self.Language, property.Name.lower(), n)}")
        for propertyid, property in self.Class.Properties.Data.items():
            n = n + 1
            params.append(f"{db.GetParameter(self.Language, property.Name.lower(), n)}")
        params_string = ", ".join(params)
        s.w(f"private static string Get{self.Class.Name}ColumnParameters() ").o()
        s.wln(f'string parameters = "{params_string}";')
        s.wln("return parameters;")
        s.c()
        s.ret()
        return s

    def writeCreateForeignKeys(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        if db.SeparateForeignKeyCreation():
            s.w(f"private static List<string> Get{self.Class.Name}ForeignKeyQueries({iid}) ").o()
            s = self.writeGetTableName(s)

            s.wln("List<string> foreignkeyqueries = new List<string>();")
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if property.ForeignKey is not None:
                        create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "%s")
                        s.wln(f'foreignkeyqueries.Add(string.Format("{create_fk}", tableName));')
                        

            for propertyid, property in self.Class.Properties.Data.items():
                if property.ForeignKey is not None:
                    create_fk = db.GetCreateForeignKeyQuery(schema, self.Class, property, property.ForeignKey, "%s")
                    s.wln(f'foreignkeyqueries.Add(string.Format("{create_fk}", tableName));')
            s.writeline("return foreignkeyqueries;")
            s.c()
            s.ret()

            s.w(f"public static void Create{self.Class.Name}ForeignKeys({conobjclass} config{iid2}) ").o()
            s.wln(f"List<string> foreignkeyqueries = {self.getDLClassName()}.Get{self.Class.Name}ForeignKeyQueries({iin});")
            s.w(f"foreach (string foreignkeyquery in foreignkeyqueries) ").o()
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteNonQuery(config, foreignkeyquery);")
            s.c()
            s.c()
            s.ret()
        return s

    def writeInsertItem(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()

        s.w(f"private static string Get{self.Class.Name}InsertQuery({iid}) ").o()
        s = self.writeGetTableName(s)
        s.wln(f'string columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames();')
        s.wln(f"string parameters = {self.getDLClassName()}.Get{self.Class.Name}ColumnParameters();")
        s.wln(f'string insertquery = $"INSERT INTO {{tableName}} ({{columns}}) VALUES ({{parameters}}){db.EndQuery()}";')
        s.wln("return insertquery;")
        s.c().ret()


        s.wln(f"private static Dictionary<string, Dictionary<string, object>> Parameterize{self.Class.Name}({self.Class.Name} {self.Class.Name.lower()})").o()
        s.wln("Dictionary<string, Dictionary<string, object>> parameters = new Dictionary<string, Dictionary<string, object>>();")
        s.wln("string param_value_key = \"Value\";")
        s.wln("string param_dbtype_key = \"DbType\";")
        n = 0
        if self.Class.InheritsFrom is not None:
            for propertyid, property in self.Class.InheritedProperties.Data.items():
                n = n + 1
                prop_val = f"{self.Class.Name.lower()}.{property.Name}"
                converted = property.To(self.Language, self.Database, n, self.Class.Name.lower(), property.Name)

                parameter_name = f"{db.GetParameter(self.Language, property.Name.lower(), n)}"
                parameter_name = property.Name.lower()
                s.wln(f'parameters.Add("{parameter_name}", new Dictionary<string, object>() {{ {converted} }});')
        for propertyid, property in self.Class.Properties.Data.items():
            n = n + 1
            prop_val = f"{self.Class.Name.lower()}.{property.Name}"
            converted = property.To(self.Language, self.Database, n, self.Class.Name.lower(), property.Name)
            parameter_name = f"{db.GetParameter(self.Language, property.Name.lower(), n)}"
            parameter_name = property.Name.lower()
            s.wln(f'parameters.Add("{parameter_name}", new Dictionary<string, object>() {{ {converted} }});')
        s.wln("return parameters;")
        s.c().ret()


        s.w(f"public static int InsertSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2}) ").o()
        s.wln(f"Dictionary<string, Dictionary<string, object>> parameters = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()});")
        s.wln(f"string insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin});")
        s.wln(f"return {self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, insertquery, parameters);")
        s.c()
        s.ret()

        return s

    def writeInsertCollection(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
    
        s.w(f"public static int Insert{self.Class.SetDescription}({conobjclass} config, {self.Class.SetDescription} {self.Class.SetDescription.lower()}{iid2})").o()
        s.wln(f"List<{self.Class.Name}> {self.Class.Name.lower()}list = {self.Class.SetDescription.lower()}.toList();")
        s.wln(f"return {self.getDLClassName()}.Insert{self.Class.Name}List(config, {self.Class.Name.lower()}list{iin2});")
        s.c()
        s.ret()
            
        s.w(f"public static int Insert{self.Class.Name}List({conobjclass} config, List<{self.Class.Name}> {self.Class.Name.lower()}list{iid2})").o()
        s.wln(f"int affectedRows = 0;")
        s.w(f"foreach({self.Class.Name} {self.Class.Name.lower()} in {self.Class.Name.lower()}list)").o()
        s.wln(f"affectedRows += {self.getDLClassName()}.InsertSingle{self.Class.Name}(config, {self.Class.Name.lower()}{iin2});")
        s.c()
        s.wln("return affectedRows;")
        s.c()
        s.ret()
        return s

    def writeSelectWhere(self, s:CSharpStringWriter):

        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        orderby = self.getOrderByClause()
        s.w(f"public static string GetSelectAll{self.Class.Name}WhereQuery(string whereclause = \"WHERE 1=1\", int limit = {str(self.Class.PageSize)}, string innerquery = \"{tablename}\"{iid2})").o()
        s.wln(f"string columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames();")
        #s = self.writeInstanceStr(s)
        s.wln(f'string selectquery = $"SELECT {db.TOP("{limit}")}{{columns}} FROM {{innerquery}} {{whereclause}}{orderby}{db.LIMIT("{limit}")}{db.EndQuery()}";')
        s.wln("return selectquery;")
        s.c().ret()


        s.w(f"public static {self.Class.SetDescription} SelectAll{self.Class.Name}Where({conobjclass} config, string whereclause = \"WHERE 1=1\", int limit = {str(self.Class.PageSize)}, string innerquery = \"{tablename}\"{iid2})").o()
        s.wln("Dictionary<string, Dictionary<string, object>> parameters = new Dictionary<string, Dictionary<string, object>>();")
        s.wln(f"string selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}WhereQuery(whereclause, limit, innerquery{iin2});")
        s.wln(f"{self.Class.SetDescription} result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, parameters);")
        s.wln(f"return result;")
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

    def writeUpdate(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()
            s.w(f"public static string Get{self.Class.Name}UpdateQuery({iid})").o()
            s.wln(f'string whereclause = " WHERE {db.OB()}{pk.Name}{db.CB()} = {db.GetParameter(self.Language, pk.Name.lower())}{db.EndQuery()}";')
            s = self.writeGetTableName(s)
            s.wln(f'string updatequery = $"UPDATE {{tableName}} SET ";')
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if not property.IsPrimaryKey:
                        s.wln(f'updatequery += "{db.OB()}{property.Name}{db.CB()} = {db.GetParameter(self.Language, property.Name.lower())},";')
            for propertyid, property in self.Class.Properties.Data.items():
                if not property.IsPrimaryKey:
                    s.wln(f'updatequery += "{db.OB()}{property.Name}{db.CB()} = {db.GetParameter(self.Language, property.Name.lower())},";')
            s.wln(f'updatequery = updatequery.Remove(updatequery.Length-1) + " " + whereclause;')
            s.wln("return updatequery;")
            s.c().ret()

            s.w(f"public static int UpdateSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2})").o()
            s.wln(f"Dictionary<string, Dictionary<string, object>> parameters = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()});")
            s.wln(f"string updatequery = {self.getDLClassName()}.Get{self.Class.Name}UpdateQuery({iin});")
            s.wln(f"return {self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, updatequery, parameters);")
            s.c()
            s.ret()


        return s

    def writePersistRecord(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        if self.Class.hasPrimaryKeyPoperty():
            pk = self.Class.getPrimaryKeyProperty()

            s.w(f"public static {pk.PropertyType(self.Language)} PersistSingle{self.Class.Name}({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}{iid2})").o()
            s.wln(f'string whereclause = "WHERE {db.OB()}{pk.Name}{db.CB()} = {db.GetParameter(self.Language, pk.Name.lower())}";')

            s.wln(f"{pk.PropertyType(self.Language)} _{pk.Name.lower()} = {self.Class.Name.lower()}.{pk.Name};")
            s.wln(f"{self.Class.SetDescription} {self.Class.Name.lower()}_items = {self.getDLClassName()}.SelectAll{self.Class.Name}Where(config, whereclause);")
    
    
            s.w(f"if ({self.Class.Name.lower()}_items.Data.Count == 1)").o()

            s.wln(f"Dictionary<string, Dictionary<string, object>> parameters = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()});")
            s.wln(f"string updatequery = {self.getDLClassName()}.Get{self.Class.Name}UpdateQuery({iin});")
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, updatequery, parameters);")
            #s.wln(f"_{pk.Name.lower()} = _{self.Class.Name.lower()}.{pk.Name}").c()
            s.wln(f"_{pk.Name.lower()} = ({pk.PropertyType(self.Language)}) {self.Class.Name.lower()}_items.Data.Keys.First();")
            s.b("else")
            s.wln(f"Dictionary<string, Dictionary<string, object>> parameters = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()});")
            s.wln(f"string insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin});")
            s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, insertquery, parameters);")
            s.c()
            s.wln(f"return _{pk.Name.lower()};");
            s.c()
            s.ret()
            if self.Class.InheritsFrom is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
                        s = self.writePersistWhereForProperty(s, property, pk)

            for propertyid, property in self.Class.Properties.Data.items(): 
                if property.IsUnique and not property.IsPrimaryKey and (property.Type == DatatypeString().getType()):
                    s = self.writePersistWhereForProperty(s, property, pk)
        return s

    def writeSelectWhereForProperty(self, s:CSharpStringWriter, property):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()

        s.wln(f'public static {self.Class.SetDescription} SelectAll{self.Class.Name}Where{property.Name}Like({conobjclass} config, string val, int limit = {str(self.Class.PageSize)}, string innerquery="{tablename}"{iid2}) ').o()
        # if db.UsesNamedParameters(self.Language):
        #     s.wln(f"params = {{ '{property.Name.lower()}': '%' + val + '%'}}")
        # else:  
        #     s.wln(f"params = ['%' + val + '%']")
        # s.wln(f'string whereclause = "WHERE {db.OB()}{property.Name}{db.CB()} LIKE {db.GetParameter(self.Language, property.Name.lower())}";')
        s.wln(f'string whereclause = $"WHERE {db.OB()}{property.Name}{db.CB()} LIKE \'%{{val}}%\'";')
        s.wln(f"string selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}WhereQuery(whereclause, limit, innerquery{iin2});")
        s.wln("Dictionary<string, Dictionary<string, object>> parameters = new Dictionary<string, Dictionary<string, object>>();")
        s.wln(f"{self.Class.SetDescription} result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, parameters);")
        s.wln(f"return result;")
        s.c()
        s.ret()
        return s

    def writePersistWhereForProperty(self, s:CSharpStringWriter, property, pk):

        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()


        s.w(f"public static string Get{self.Class.Name}UpdateWhere{property.Name}EqualsQuery({iid2})").o()
        #s.writeline(f'innerquery = "{tablename}"')

        #s.wln(f"if whereclause is None:").o()
        s.wln(f'string whereclause = " WHERE {db.OB()}{property.Name}{db.CB()} = {db.GetParameter(self.Language, property.Name.lower())}{db.EndQuery()}";')
        s = self.writeInstanceStr(s, "\"" + tablename + "\"")
        s.wln(f'string updatequery = $"UPDATE {{innerquery}} SET ";')
        if self.Class.InheritsFrom is not None:
            for propertyid, _property in self.Class.InheritedProperties.Data.items():
                if not _property.IsPrimaryKey: 
                    if _property.ID != property.ID:
                        s.wln(f'updatequery += "{db.OB()}{_property.Name}{db.CB()} = {db.GetParameter(self.Language, _property.Name.lower())},";')
        for propertyid, _property in self.Class.Properties.Data.items():
            if not _property.IsPrimaryKey:
                if _property.ID != property.ID:
                    s.wln(f'updatequery += "{db.OB()}{_property.Name}{db.CB()} = {db.GetParameter(self.Language, _property.Name.lower())},";')
        s.wln(f'updatequery = updatequery.Substring(0, updatequery.Length - 1) + " " + whereclause;')
        s.wln("return updatequery;")
        s.c().ret()


        s.w(f"public static {pk.PropertyType(self.Language)} Persist{self.Class.Name}Where{property.Name}Equals({conobjclass} config, {self.Class.Name} {self.Class.Name.lower()}) ").o()
        s.wln(f'string whereclause = $"WHERE {db.OB()}{property.Name}{db.CB()} = \'{{{self.Class.Name.lower()}.{property.Name}}}\'";');
        s.wln(f"{pk.PropertyType(self.Language)} _{pk.Name.lower()} = {self.Class.Name.lower()}.{pk.Name};")
        s.wln(f"{self.Class.SetDescription} {self.Class.Name.lower()}_items = {self.getDLClassName()}.SelectAll{self.Class.Name}Where(config, whereclause);")


        s.w(f"if ({self.Class.Name.lower()}_items.Data.Count == 1)").o()
            
        s.wln(f"Dictionary<string, Dictionary<string, object>> parameters = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()});")
        s.wln(f"string updatequery = {self.getDLClassName()}.Get{self.Class.Name}UpdateWhere{property.Name}EqualsQuery({iin});")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, updatequery, parameters);")
        s.wln(f"_{pk.Name.lower()} = {self.Class.Name.lower()}_items.toList()[0].{pk.Name};")
        s.b("else")
        s.wln(f"Dictionary<string, Dictionary<string, object>> parameters = {self.getDLClassName()}.Parameterize{self.Class.Name}({self.Class.Name.lower()});")
        s.wln(f"string insertquery = {self.getDLClassName()}.Get{self.Class.Name}InsertQuery({iin});")
        s.wln(f"{self.CommonFunctionsClassName}.ExecuteParameterizedNonQuery(config, insertquery, parameters);")
        s.c()
        s.wln(f"return _{pk.Name.lower()};")
        s.c()
        s.ret()


        return s


    def writeSelectAll(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        orderby = self.getOrderByClause()
        readerclass = db.ReaderClass(self.Language)

        s.w(f'public static string GetSelectAll{self.Class.Name}Query(int limit={str(self.Class.PageSize)}, string innerquery="{tablename}"{iid2}) ').o()
        s.wln(f"string columns = {self.getDLClassName()}.Get{self.Class.Name}ColumnNames();")
        #s = self.writeInstanceStr(s)
        s.wln(f'string selectquery = $"SELECT {db.TOP("{limit}")}{{columns}} FROM {{innerquery}}{orderby}{db.LIMIT("{limit}")}{db.EndQuery()}";')
        s.wln("return selectquery;")
        s.c().ret()


        s.w(f'public static {self.Class.SetDescription} SelectAll{self.Class.Name}({conobjclass} config, int limit={str(self.Class.PageSize)}, string innerquery="{tablename}"{iid2}) ').o()
        # if db.UsesNamedParameters(self.Language):
        #     s.wln(f"parameters = {{ }}")
        # else:  
        #     s.wln(f"parameters = []")
        s.wln("Dictionary<string, Dictionary<string, object>> parameters = new Dictionary<string, Dictionary<string, object>>();")
        s.wln(f"string selectquery = {self.getDLClassName()}.GetSelectAll{self.Class.Name}Query(limit, innerquery{iin2});")
        s.wln(f"{self.Class.SetDescription} result = {self.getDLClassName()}.Select{self.Class.SetDescription}(config, selectquery, parameters);")
        s.wln(f"return result;")
        s.c()
        s.ret()


        s.w(f"public static {self.Class.SetDescription} Select{self.Class.SetDescription}({conobjclass} config, string selectquery, Dictionary<string, Dictionary<string, object>> parameters) ").o()
        s.wln(f"Func<{readerclass}, object> translation = {self.getDLClassName()}.Get{self.Class.Name}FromQueryResult;")
        s.wln(f"List<{self.Class.Name}> _{self.Class.Name.lower()}_list = {self.CommonFunctionsClassName}.ExecuteFetchAll(config, selectquery, parameters, translation).Cast<{self.Class.Name}>().ToList();;")
        s.wln(f"{self.Class.SetDescription} {self.Class.Name.lower()}_list = new {self.Class.SetDescription}().fromList(_{self.Class.Name.lower()}_list);")
        s.wln(f"return {self.Class.Name.lower()}_list;")
        s.c()
        s.ret()
        return s

    def writeSelectSingleRecordByPK(self, s:CSharpStringWriter):
        (db, schema, tablename, iid, iid2, iin, iin2, conobjclass) = self.getCommonItems()
        orderby = self.getOrderByClause()
        readerclass = db.ReaderClass(self.Language)

        s.w(f"public static object Get{self.Class.Name}FromQueryResult({readerclass} reader) ").o()
        s.wln(f"{self.Class.Name} {self.Class.Name.lower()} = new {self.Class.Name}(")
        s.Inc()
        index = 0
        if self.Class.InheritsFrom is not None:
            if self.Class.InheritedProperties is not None:
                for propertyid, property in self.Class.InheritedProperties.Data.items():
                    converted = property.From(self.Language, self.Database, f"reader[\"{property.Name}\"]")
                    s.wln(f"{property.Name.lower()}: {converted},")
        for propertyid, property in self.Class.Properties.Data.items():
            converted = property.From(self.Language, self.Database, f"reader[\"{property.Name}\"]")
            s.wln(f"{property.Name.lower()}: {converted},")
        s.rem(2)
        s.Dec()
        s.wln(");")
        s.wln(f"return (object){self.Class.Name.lower()};")
        s.c()
        s.ret()

        return s
