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
    INHERITSFROMID = "InheritsFromID"
    INHERITSFROM = "InheritsFrom"
    PLURALNAME = "PluralName"
    SETDESCRIPTION = "SetDescription"
    PAGESIZE = "PageSize"
    CLONEABLE = "Cloneable"

  class PropertID():
    TYPE = "1fefc4f1-a3da-4c55-a5c5-2332e1330a07"
    NAME = "5c44f1d6-45ef-4cf7-848b-efda7e417d56"
    DESCRIPTION = "d72d62ff-2d93-4d82-bc30-37f927501b8b"
    ID = "93037bdc-ccd6-4c06-9473-ab2a39d56d1b"
    PARENTMODLUE = "1ab7f6b9-635c-48ec-929f-3d041e34dcee" 
    PROPERTIES = "b95a7a80-21b8-417f-862c-49365faa94d0"
    INHERITSFROMID = "987d435c-3726-488e-a627-34080d055bc5"
    INHERITSFROM = "d23ce36a-2950-49a7-a008-1c935f7678b4"
    PLURALNAME = "c28bb6ff-6de2-4180-a379-207626961090"
    SETDESCRIPTION = "74a0b9e3-2589-4e6a-93eb-6baa5f3eff8a"
    PAGESIZE = "3ab655f0-ac2c-4242-8573-a0b42f5925ad"
    CLONEABLE = "625b0914-1d25-43c5-ade2-1eb3f2db842c"
  
  def __init__(self):
    self.Type = "toren.Class"
    self.Name = ""
    self.Description = ""
    self.SetDescription = self.getSetDescription(self.Name)
    self.ID = ""
    self.ParentModule = None
    self.Properties = DatatypeCollection()
    self.setInheritsFrom(None)
    self.PluralName = self.getDefaultPluralName(self.Name, None)
    

  def getDefaultPluralName(self, name, pluralname=None):
    if pluralname is not None:
      return pluralname
    return f"{name}Set"

  def getSetDescription(self, name):
    return f"{name}Collection"

  def initialize(self, 
                 name: str, 
                 description: str, 
                 id: str,
                 properties: List[Datatype] = None,
                 inheritsfrom = None,
                 pluralname = None,
                 pageSize: int = 1000,
                 cloneable: bool = False):
    self.Type = "toren.Class"
    self.IsInReservedNames(name)
    self.Name = name
    self.Description = description
    self.SetDescription = self.getSetDescription(self.Name)
    self.PluralName = self.getDefaultPluralName(self.Name, pluralname)
    self.ID = id
    self.ParentModule = None
    self.setInheritsFrom(inheritsfrom)
    self.Properties = DatatypeCollection().initialize(properties, self) #self.setProperties(properties)
    self.PageSize = pageSize
    self.Cloneable = cloneable
    return self
  
  def getInheritedProperties_(self, _class, _properties):
    if _class.InheritsFrom is not None:
      _properties = _properties.addCollection(_class.InheritsFrom.Properties)
      _properties = _class.InheritsFrom.getInheritedProperties(_class.InheritsFrom, _properties)
      return _properties

    return _properties
  
  def getInheritedProperties(self, _class, _properties):
    inheritance_chain = _class.getInheritanceChain()
    for parent_class in reversed(inheritance_chain):
      _properties = _properties.addCollection(parent_class.Properties)
    return _properties
  
  def getInheritanceChain(self):
    inheritance_chain = []
    if self.InheritsFrom is not None:
      inheritance_chain.append(self.InheritsFrom)
      inheritance_chain.extend(self.InheritsFrom.getInheritanceChain())
    
    return inheritance_chain
    
  def IsInReservedNames(self, name):
    if name in self.ReservedClassNames():
      raise Exception(f"Class name '{name}' is in reserved list") 
      return True
    
    return False

  def ReservedClassNames(self):
    return ["Connection", "Class", "Common"]
  
  def getProperties(self, includeInheritance=False):
    properties = self.Properties
    if includeInheritance:
      properties = self.getInheritedProperties(self, properties)
    return properties
  

  def hasPrimaryKeyPoperty(self):
    for propertyid, property in self.InheritedProperties.Data.items():
      if property.IsPrimaryKey:
        return True
    for propertyid, property in self.Properties.Data.items():
      if property.IsPrimaryKey:
        return True
    return False
  
  def getPrimaryKeyProperty(self):
    for propertyid, property in self.InheritedProperties.Data.items():
      if property.IsPrimaryKey:
        return property
    for propertyid, property in self.Properties.Data.items():
      if property.IsPrimaryKey:
        return property
    return None

  def setInheritsFrom(self, inheritsFromClass):

    if inheritsFromClass is not None:
      self.InheritsFrom = inheritsFromClass
      self.InheritsFromID = inheritsFromClass.ID
      self.InheritedProperties = self.getInheritedProperties(self, DatatypeCollection())
      #self.InheritedProperties = self.getProperties(True)
    else:
      self.InheritsFrom = inheritsFromClass
      self.InheritsFromID = None
      self.InheritedProperties = DatatypeCollection()
    return self

  def setParentModule(self, parentModule):
    self.ParentModule = parentModule
    return self

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
    _class[self.PropertName.PLURALNAME] = self.PluralName
    _class[self.PropertName.SETDESCRIPTION] = self.SetDescription
    _class[self.PropertName.DESCRIPTION] = self.Description
    _class[self.PropertName.ID]  = self.ID
    _class[self.PropertName.INHERITSFROMID] = self.InheritsFromID
    _class[self.PropertName.PAGESIZE] = self.PageSize
    _class[self.PropertName.CLONEABLE] = self.Cloneable
    _class[self.PropertName.PROPERTIES] = self.Properties.to_list_of_dict()
    return _class
  
  def from_dict(self, _class):
    #self.Type = str(_class[self.PropertName.TYPE])
    self.Name = str(_class[self.PropertName.NAME])
    self.PluralName = str(_class[self.PropertName.PLURALNAME])
    self.Description = str(_class[self.PropertName.DESCRIPTION])
    self.SetDescription = str(_class[self.PropertName.SETDESCRIPTION])
    self.ID = str(_class[self.PropertName.ID])
    self.InheritsFromID = _class[self.PropertName.INHERITSFROMID] if self.PropertName.INHERITSFROMID in _class else None
    self.PageSize = int(_class[self.PropertName.PAGESIZE])
    self.Cloneable = bool(_class[self.PropertName.CLONEABLE])
    self.Properties = DatatypeCollection().initialize(_class[self.PropertName.PROPERTIES], self)
    return self


  def get_sub_classes(self, _sub_classes={}):
    for _classid, _class in self.ParentModule.Classes.Data.items():
        if _class.InheritsFromID == self.ID:
            _sub_classes[_class.ID] = _class
            _sub_classes = _class.get_sub_classes(_sub_classes)
    
    return _sub_classes
      
     

  def get_linked_foreign_keys(self, includedinheritance=False):
    _linked_foreign_keys = collections.OrderedDict() 
               
    for _classid, _class in self.ParentModule.Classes.Data.items():
        for _propertyid, _property in _class.Properties.Data.items():
            if _property.ForeignKey is not None:
                if _property.ForeignKey.FKClassID == self.ID:
                    _linked_foreign_keys[_property.ID] = _property

    if includedinheritance:
      for _classid, _class in self.ParentModule.Classes.Data.items():
          for _propertyid, _property in _class.InheritedProperties.Data.items():
              if _property.ForeignKey is not None:
                  if _property.ForeignKey.FKClassID == self.ID:
                      _linked_foreign_keys[_property.ID] = _property

    return _linked_foreign_keys

  def get_linked_foreign_key_classes(self, includedinheritance=False):
    _linked_foreign_key_classes = collections.OrderedDict() 
               
    for _classid, _class in self.ParentModule.Classes.Data.items():
        for _propertyid, _property in _class.Properties.Data.items():
            if _property.ForeignKey is not None:
                if _property.ForeignKey.FKClassID == self.ID:
                    _linked_foreign_key_classes[_class.ID] = _class

    if includedinheritance:
      for _classid, _class in self.ParentModule.Classes.Data.items():
          for _propertyid, _property in _class.InheritedProperties.Data.items():
              if _property.ForeignKey is not None:
                  if _property.ForeignKey.FKClassID == self.ID:
                      _linked_foreign_key_classes[_class.ID] = _class

    return _linked_foreign_key_classes
