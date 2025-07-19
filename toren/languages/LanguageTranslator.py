from ..TorenObject import TorenObject
import collections
import json

from .Language import Language
from .LanguagePython import LanguagePython
from ..datastores.Database import Database
from ..datastores.DatabaseSQLite import DatabaseSQLite

class LanguageTranslator(TorenObject):

  class PropertName():
    TYPE = "Type"
    NAME = "Name"
    DESCRIPTION = "Description"
    ID = "ID"
    LANGUAGEID = "LanguageID"
    

  class PropertID():
    TYPE = "f09c2957-481d-4f7e-8727-28205ecf917a"
    NAME = "5564013b-551a-4faa-b3b0-a223f1108ee4"
    DESCRIPTION = "25023ef9-372b-4504-b4a5-520945a326f8"
    ID = "a1a3c8f4-e232-44b7-8b47-d005862c69e"
    LANGUAGEID = "d2d2f247-457b-440a-a9fd-7f3dfdb031fa" 

  def __init__(self, 
               name, 
               desc, 
               language: Language):
    self.Type = self.getType()
    self.Name = name
    self.Description = desc
    self.ID = self.getID()
    self.Language = language
    self.LanguageID = language.ID

  def getType(self):
    return "toren.languages.LanguageTranslator"
  
  def getID(self):
    return "80a0b393-0272-477a-b5e9-9f5ceb3a31d0"
  


  
  