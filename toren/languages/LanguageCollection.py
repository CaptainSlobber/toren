from ..TorenObject import TorenObject
from .Language import Language
from .LanguagePython import LanguagePython
from .LanguageCSharp import LanguageCSharp
from .LanguageGo import LanguageGo
from .LanguageJava import LanguageJava
from .LanguageJavaScript import LanguageJavaScript
import collections
import json
from typing import List


class LanguageCollection():

    def getType(self):
        return "toren.languages.LanguageCollection"
    
    def __init__(self):
        self.Data = collections.OrderedDict()

    
    def initialize(self, languagelist: List[Language] = [], parentproject = None):
        self.from_list(languagelist, parentproject)
        return self

    
    def addLanguage(self, language, languagecollection, parentproject):
        if isinstance(language, dict): 

            languageclassname=language["Type"].split(".")[-1]

            match languageclassname:
                case "LanguagePython": language = LanguagePython().from_dict(language)
                case "LanguageCSharp": language = LanguageCSharp().from_dict(language)
                case "LanguageGo": language = LanguageGo().from_dict(language)
                case "LanguageJava": language = LanguageJava().from_dict(language)
                case "LanguageJavaScript": language = LanguageJavaScript().from_dict(language)

        language.setParentProject(parentproject)
        languagecollection[language.ID] = language
        return languagecollection

    def from_list(self, languagelist: List[Language] = [], parentproject =None):
        _languages = collections.OrderedDict()
        if not languagelist is None:
            for language in languagelist:
                _languages = self.addLanguage(language, _languages, parentproject)
        self.Data = _languages
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [l.to_dict() for l in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, languages: dict, parentproject =None):
        _languages = collections.OrderedDict()
        if not languages is None:
            for key, value in languages.items():
                _languages = self.addLanguage(value, _languages, parentproject)
        self.Data = _languages
        return self  
                