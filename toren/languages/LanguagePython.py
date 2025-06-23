from .Language import Language
import collections

class LanguagePython(Language):
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()

  def getDefaultFileExtension(self):
    return "py"

  def getName(self):
    return "Python"
  
  def getDescription(self):
    return "Python"

  def getType(self):
    return "toren.languages.LanguagePython"
  
  def getID(self):
    return "bddf1d35-ffdd-46fc-9720-6f144f4a7bdc"

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = self.getName()
    self.Description = self.getDescription()
    self.ID = self.getID()
    self.DefaultFileExtension = self.getDefaultFileExtension()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    return self