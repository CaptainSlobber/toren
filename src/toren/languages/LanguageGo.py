from .Language import Language
import collections

class LanguageGo(Language):
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()


  def getDefaultFileExtension(self):
    return "go"
  
  def getName(self):
    return "Go"
  
  def getDescription(self):
    return "Go"

  def getType(self):
    return "toren.languages.LanguageGo"
  
  def getID(self):
    return "d79039f7-419b-41a2-9793-12dc9932f01f"

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    return self