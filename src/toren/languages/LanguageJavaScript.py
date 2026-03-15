from .Language import Language
import collections

class LanguageJavaScript(Language):
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()

  def getDefaultFileExtension(self):
    return "js"

  def getName(self):
    return "JavaScript"
  
  def getDescription(self):
    return "JavaScript"

  def getType(self):
    return "toren.languages.LanguageJavaScript"
  
  def getID(self):
    return "3ff4db70-2505-4c9e-90d6-e6f221ad8bd8"

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    return self