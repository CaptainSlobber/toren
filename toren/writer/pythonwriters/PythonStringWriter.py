
import os
from pathlib import Path

from typing import List
from ...languages import *
from ..StringWriter import StringWriter


class PythonStringWriter(StringWriter):

    def __init__(self, language: Language, indent: int = 4):
        super().__init__(language=language)
        self.Language = language
        self.I = ' ' * indent

    def o(self):
        self.Inc()
        return self

    
    def c(self):
        self.Dec()
        self.write(self.newline())
        return self
        

