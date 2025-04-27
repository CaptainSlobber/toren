from .TorenObject import TorenObject
from .datatypes import *
import collections
import json
from typing import List



class Class(TorenObject):


  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    PARENTMODLUE = "ParentModule"
    PROPERTIES = "Properties"

  class PropertID():
    TYPE = "1fefc4f1-a3da-4c55-a5c5-2332e1330a07"
    NAME = "5c44f1d6-45ef-4cf7-848b-efda7e417d56"
    DESCRIPTION = "d72d62ff-2d93-4d82-bc30-37f927501b8b"
    ID = "93037bdc-ccd6-4c06-9473-ab2a39d56d1b"
    PARENTMODLUE = "1ab7f6b9-635c-48ec-929f-3d041e34dcee" 
    PROPERTIES = "b95a7a80-21b8-417f-862c-49365faa94d0"
  
  def __init__(self):
    self.Type = "toren.Class"
    self.Name = ""
    self.Description = ""
    self.ID = ""
    self.ParentModule = None
    self.Properties = []


  def initialize(self, 
                 name: str, 
                 description: str, 
                 id: str,
                 properties: List[Datatype] = None):
    self.Type = "toren.Class"
    self.Name = name
    self.Description = description
    self.ID = id
    self.ParentModule = None
    self.Properties = self.setProperties(properties)
    return self

  def setProperties(self, properties):
    return self.setPropertiesFromList(properties)
  
  def setPropertiesFromList(self, properties):
    _properties = collections.OrderedDict()
    if not properties is None:
      for property in properties:
        if isinstance(property, dict): 
          #property = Datatype().from_dict(property)
          propclassname=property["Type"].split(".")[-1]

          match propclassname:

            case "DatatypeNumeric": property = DatatypeNumeric().from_dict(property)
            case "DatatypeCharacter": property = DatatypeCharacter().from_dict(property)
            case "DatatypeString": property = DatatypeString().from_dict(property)
            case "DatatypeUUID": property = DatatypeUUID().from_dict(property)
            case "DatatypeBigInt": property = DatatypeBigInt().from_dict(property)
            case "DatatypeInt": property = DatatypeInt().from_dict(property)
            case "DatatypeBinary": property = DatatypeBinary().from_dict(property)
            case "DatatypeSmallInt": property = DatatypeSmallInt().from_dict(property)
            case "DatatypeDecimal": property = DatatypeDecimal().from_dict(property)
            case "DatatypeBoolean": property = DatatypeBoolean().from_dict(property)
            case "DatatypeFloat": property = DatatypeFloat().from_dict(property)
            case "DatatypeDouble": property = DatatypeDouble().from_dict(property)
            case "DatatypeNetworkAddress": property = DatatypeNetworkAddress().from_dict(property)
            case "DatatypeDatetime": property = DatatypeDatetime().from_dict(property)
                            
        property.setParentClass(self)
        _properties[property.ID] = property
    return _properties

  def setParentModule(self, parentModule):
    self.ParentModule = parentModule

  def to_json(self):
    _module_json = json.dumps(self.to_dict())
    return _module_json

  def from_json(self, jsonString):
    _class = json.loads(jsonString)
    self.from_dict(_class)
    return self
  
  def to_dict(self):
    _class = {}
    _class[self.PropertName.TYPE] = self.Type
    _class[self.PropertName.NAME] = self.Name
    _class[self.PropertName.DESCRIPTION] = self.Description
    _class[self.PropertName.ID]  = self.ID
    _class[self.PropertName.PROPERTIES] = [p.to_dict() for p in list(self.Properties.values())]

    return _class
  
  def from_dict(self, _class):
    #self.Type = str(_class[self.PropertName.TYPE])
    self.Name = str(_class[self.PropertName.NAME])
    self.Description = str(_class[self.PropertName.DESCRIPTION])
    self.ID = str(_class[self.PropertName.ID])
    self.Properties = self.setProperties(_class[self.PropertName.PROPERTIES])
    return self
