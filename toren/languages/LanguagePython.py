from .Language import Language
import collections

class LanguagePython(Language):
  
  def __init__(self):
    self.Type = self.getType()
    self.Name = "Python"
    self.Description = "Python"
    self.ID = self.getID()

  def __init__(self):
    self.initialize()

  def getType(self):
    return "toren.languages.LanguagePython"
  
  def getID(self):
    return "bddf1d35-ffdd-46fc-9720-6f144f4a7bdc"

  def initialize(self, outputdirectory=""):
    self.Type = self.getType()
    self.Name = "Python"
    self.Description = "Python"
    self.ID = self.getID()
    self.ParentProject = None
    self.OutputDirectory = outputdirectory
    return self