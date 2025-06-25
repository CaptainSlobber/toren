
import os
from pathlib import Path

from typing import List
from ...languages import *
from ..StringWriter import StringWriter


class JavaScriptStringWriter(StringWriter):

    def __init__(self, language: Language):
        super().__init__(language=language)
        self.Language = language
        self.I = ' ' * 3