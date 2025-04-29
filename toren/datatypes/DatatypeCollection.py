from ..TorenObject import TorenObject
from .Datatype import Datatype
from .DatatypeNumeric import DatatypeNumeric
from .DatatypeCharacter import DatatypeCharacter
from .DatatypeString import DatatypeString
from .DatatypeUUID import DatatypeUUID
from .DatatypeBigInt import DatatypeBigInt
from .DatatypeInt import DatatypeInt
from .DatatypeSmallInt import DatatypeSmallInt
from .DatatypeBinary import DatatypeBinary
from .DatatypeDecimal import DatatypeDecimal
from .DatatypeBoolean import DatatypeBoolean
from .DatatypeFloat import DatatypeFloat
from .DatatypeDouble import DatatypeDouble
from .DatatypeNetworkAddress import DatatypeNetworkAddress
from .DatatypeDatetime import DatatypeDatetime
import collections
import json
from typing import List


class DatatypeCollection():

    def getType(self):
        return "toren.datatypes.DatatypeCollection"
    
    def __init__(self):
        self.Data = collections.OrderedDict()

    
    def initialize(self, datatypelist: List[Datatype] = [], parentclass = None):
        self.from_list(datatypelist, parentclass)
        return self

    def removeDatatype(self, key):
        if key in self.Data:
            del self.Data[key]

    def addDatatype(self, datatype, parentclass):
        if isinstance(datatype, dict): 
            datatypeclassname=datatype["Type"].split(".")[-1]

            match datatypeclassname:
                case "DatatypeNumeric": datatype = DatatypeNumeric().from_dict(datatype)
                case "DatatypeCharacter": datatype = DatatypeCharacter().from_dict(datatype)
                case "DatatypeString": datatype = DatatypeString().from_dict(datatype)
                case "DatatypeUUID": datatype = DatatypeUUID().from_dict(datatype)
                case "DatatypeBigInt": datatype = DatatypeBigInt().from_dict(datatype)
                case "DatatypeInt": datatype = DatatypeInt().from_dict(datatype)
                case "DatatypeBinary": datatype = DatatypeBinary().from_dict(datatype)
                case "DatatypeSmallInt": datatype = DatatypeSmallInt().from_dict(datatype)
                case "DatatypeDecimal": datatype = DatatypeDecimal().from_dict(datatype)
                case "DatatypeBoolean": datatype = DatatypeBoolean().from_dict(datatype)
                case "DatatypeFloat": datatype = DatatypeFloat().from_dict(datatype)
                case "DatatypeDouble": datatype = DatatypeDouble().from_dict(datatype)
                case "DatatypeNetworkAddress": datatype = DatatypeNetworkAddress().from_dict(datatype)
                case "DatatypeDatetime": datatype = DatatypeDatetime().from_dict(datatype)
                            
        datatype.setParentClass(parentclass)
        self.Data[datatype.ID] = datatype

    def from_list(self, datatypelist: List[Datatype] = [], parentclass =None):
        self.Data = collections.OrderedDict()
        if not datatypelist is None:
            for datatype in datatypelist:
                self.addDatatype(datatype, parentclass)
        return self
    
    def to_list(self):
        return list(self.Data.items())
    
    def to_list_of_dict(self):
        return [p.to_dict() for p in list(self.Data.values())]
    
    def to_dict(self):

        return dict(self.Data)
        
    def from_dict(self, datatypes: dict, parentclass =None):
        self.Data = collections.OrderedDict()
        if not datatypes is None:
            for key, value in datatypes.items():
                self.addDatatype(value, parentclass)
        return self  
                
