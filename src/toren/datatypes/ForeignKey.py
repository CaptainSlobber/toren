

import collections
import json

class ForeignKey():



    class PropertName():
        FKCLASS = "FKClass"
        FKCLASSID = "FKClassID"
        FKCLASSPROPERTY = "FKClassProperty"
        FKCLASSPROPERTYID = "FKClassPropertyID"
        PROPERTYNAME = "FKPropertyName"

    class PropertID():
        FKCLASS = "322c8d83-0854-4abf-9c0d-078253a9fff9"
        FKCLASSID = "db5c896b-1670-4d9c-942f-2290f525f0b3"
        FKCLASSPROPERTY = "8ccec448-1ebd-4837-94cd-451edf269391"
        FKCLASSPROPERTYID = "e1e40be8-7ad5-4706-bd07-baf84d3bd324"
        PROPERTYNAME = "52a5dba2-c679-452a-82b4-de0e2c59e437"

    def getType(self):
        return "toren.datatypes.ForeignKey"
      
    def __init__(self):
        pass


    def initialize(self, foreignkeypropertyname:str, foreignkeyclassproperty, foreignkeyclass=None):
        self.Type = self.getType()

        self.FKClassProperty = foreignkeyclassproperty
        self.FKClassPropertyID = foreignkeyclassproperty.ID
        self.PropertyName = foreignkeypropertyname

        if foreignkeyclass is not None:
            self.FKClass = foreignkeyclass
            self.FKClassID = foreignkeyclass.ID
        else:
            self.FKClass = foreignkeyclassproperty.ParentClass
            self.FKClassID = foreignkeyclassproperty.ParentClass.ID
        return self

    def from_dict(self, fk):
        self.Type = self.getType()
        self.FKClass = None
        self.FKClassID = str(fk[self.PropertName.FKCLASSID])
        self.FKClassProperty = None
        self.FKClassPropertyID = str(fk[self.PropertName.FKCLASSPROPERTYID])
        self.PropertyName = str(fk[self.PropertName.PROPERTYNAME])
        return self

    def to_dict(self):
        _fk = {}
        _fk[self.PropertName.FKCLASSID] = self.FKClassID
        _fk[self.PropertName.FKCLASSPROPERTYID] = self.FKClassPropertyID
        _fk[self.PropertName.PROPERTYNAME] = self.PropertyName
        return _fk
    
    def to_json(self):
        _fk_json = json.dumps(self.to_dict())
        return _fk_json

    def from_json(self, jsonString):
        _fk = json.loads(jsonString)
        self.from_dict(_fk)
        return self
    