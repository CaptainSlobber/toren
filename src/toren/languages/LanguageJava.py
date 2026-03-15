from .Language import Language
import collections

class LanguageJava(Language):
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()

  def getDefaultFileExtension(self):
    return "java"

  def getName(self):
    return "Java"
  
  def getDescription(self):
    return "Java"

  def getType(self):
    return "toren.languages.LanguageJava"
  
  def getID(self):
    return "73bebab6-c6b6-46f3-8a5f-36f6524b988c"

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    return self