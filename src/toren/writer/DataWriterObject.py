
from ..datastores.Database import Database
from ..Project import Project
from ..Module import Module
from ..Class import Class
from ..languages import *
from ..tracer.Logger import Logger
from .WriterObject import WriterObject

class DataWriterObject(WriterObject):

    def __init__(self):
        #self.Logger = Logger()
        pass

    def getDLPrefix(self):
        return "DL"
    
    def getDLSuffix(self):
        return ""