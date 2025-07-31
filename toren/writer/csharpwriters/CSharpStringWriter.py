
import os
from pathlib import Path

from typing import List
from ...languages import *
from ..StringWriter import StringWriter


class CSharpStringWriter(StringWriter):

    def __init__(self, language: Language, indent: int = 3):
        super().__init__(language=language)
        self.Language = language
        self.I = ' ' * indent

    def o(self):
        self.append("{").Inc()
        return self

    
    def c(self):
        self.Dec()
        self.append("}")
        self.append(self.newline())
        return self
        

