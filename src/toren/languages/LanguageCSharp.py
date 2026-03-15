from .Language import Language
import collections

class LanguageCSharp(Language):
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()

  def getDefaultFileExtension(self):
    return "cs"

  def getName(self):
    return "CSharp"
  
  def getDescription(self):
    return "C#"

  def getType(self):
    return "toren.languages.LanguageCSharp"
  
  def getID(self):
    return "380b4048-41d5-4978-9c21-1328f222a6d4"

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    return self