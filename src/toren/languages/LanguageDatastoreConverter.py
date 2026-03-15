from ..TorenObject import TorenObject
from .Language import Language
from ..datastores.Database import Database
import collections
import json

class LanguageDatastoreConverter(TorenObject):

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    LANGUAGEID = "LanguageID"
    DATASTOREID = "DatastoreID"
    

  class PropertID():
    TYPE = "fa23b094-df0f-4bc2-aedf-7f7a30aeb179"
    NAME = "1fabcc63-a232-4ba7-aaf0-e7f8521b84be"
    DESCRIPTION = "949891b1-1d19-4e10-a437-5792547a815e"
    ID = "5afa4244-a6bb-4dae-9ec4-39524cee767f"
    LANGUAGEID = "5a67f1e6-e7f5-45c1-82bb-21909e4e3182" 
    DATASTOREID = "26de7ba6-69a3-45f1-a156-f04c1b9da765"


  def __init__(self, 
               name, 
               desc, 
               language: Language, 
               datastore: Database):
    self.Type = self.getType()
    self.Name = name
    self.Description = desc
    self.ID = self.getID()
    self.Language = language
    self.LanguageID = language.ID
    self.Datastore = datastore
    self.DatastoreID = datastore.ID
    self.FromDatastore = None
    self.ToDatastore = None

  def getType(self):
    return "toren.languages.LanguageDatastoreConverter"
  
  def getID(self):
    return "92e8a8aa-9092-4309-ab6b-6f8b2ba50b71"
  

