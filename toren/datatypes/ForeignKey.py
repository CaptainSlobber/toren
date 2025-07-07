

import collections
import json

class ForeignKey():



    class PropertName():
        FKCLASS = "FKClass"
        FKCLASSID = "FKClassID"
        FKFIELD = "FKField"
        FKFIELDID = "FKFieldID"

    class PropertID():
        FKCLASS = "FKClass"
        FKCLASSID = "FKClassID"
        FKFIELD = "FKField"
        FKFIELDID = "FKFieldID"

    def getType(self):
        return "toren.datatypes.ForeignKey"
      
    def __init__(self):
        pass


    def initialize(self, foreignkeyproperty, foreignkeyclass=None):
        self.Type = self.getType()

        self.FKField = foreignkeyproperty
        self.FKFieldID = foreignkeyproperty.ID

        if foreignkeyclass is not None:
            self.FKClass = foreignkeyclass
            self.FKClassID = foreignkeyclass.ID
        else:
            self.FKClass = foreignkeyproperty.ParentClass
            self.FKClassID = foreignkeyproperty.ParentClass.ID
        return self

    def from_dict(self, fk):
        self.Type = self.getType()
        self.FKClass = None
        self.FKClassID = str(fk[self.PropertName.FKCLASSID])
        self.FKField = None
        self.FKFieldID = str(fk[self.PropertName.FKFIELDID])
        return self

    def to_dict(self):
        _fk = {}
        _fk[self.PropertName.FKCLASSID] = self.FKClassID
        _fk[self.PropertName.FKFIELDID] = self.FKFieldID

        return _fk
    
    def to_json(self):
        _fk_json = json.dumps(self.to_dict())
        return _fk_json

    def from_json(self, jsonString):
        _fk = json.loads(jsonString)
        self.from_dict(_fk)
        return self
    