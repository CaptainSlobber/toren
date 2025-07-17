from io import StringIO
from typing import Self
from ..languages import Language
 
class StringWriter:
    def __init__(self, language: Language):
        self.Language = language
        self._buffer = StringIO()
        self.I = ' ' * 3
        self.N = 0

    def forceString(self, value) -> str:
        """Force a value to be a string."""
        if value is None:
            return ""
        return str(value)

    def newline(self) -> str:
        return "\n"

    def o(self) -> Self:
        """Open."""
        
        self.write("{")
        self.Inc()
        return self
    
    def n(self) -> Self:
        self.write(self.newline())
        return self
    

    def Inc(self, n=1):
        self.N = self.N + n 

    def Dec(self, n = 1):
        self.N = self.N - n 
    
    def c(self) -> Self:
        """Close."""
        self.Dec()
        self.write("}")
        self.append(self.newline())
        return self
    
    def f(self) -> Self:
        """Open Function."""
        self.write("function")
        return self
    

    def append(self, text: str) -> Self:
        self._buffer.write(text)
        return self

    def write(self, text: str) -> Self:
        """Write text to the buffer."""
        self._buffer.write(self.I * self.N)
        self._buffer.write(text)
        return self
    
    def w(self, text: str): 
        return self.write(text)
    
    def writeline(self, text: str) -> Self:
        """Write text to the buffer."""
        self.write(text)
        self.append(self.newline())
        return self
    
    def rem(self, n=1) -> Self:
        """Remove the last n characters from the buffer."""
        current_value = self._buffer.getvalue()
        self._buffer.truncate(0)
        self._buffer.seek(0)
        self._buffer.write(current_value[:-n])
        return self

    def ret(self):
        return self.writeline("")
    
    def wln(self, text: str):
        return self.writeline(text)

    def flush(self) -> Self:
        """Flush the buffer."""
        self._buffer.flush()
        return self

    def seek(self, offset: int, whence: int = 0) -> Self:
        """Move the cursor to a specific position in the buffer."""
        self._buffer.seek(offset, whence)
        return self

    def read(self, size: int = -1):
        """Read a specified number of characters from the buffer."""
        return self._buffer.read(size)
    
    def readline(self):
        """Read a single line from the buffer."""
        return self._buffer.readline()
    
    def readlines(self):
        """Read all lines from the buffer."""
        return self._buffer.readlines()
    
    def truncate(self, size: int = None):
        """Truncate the buffer to a specified size."""
        if size is None:
            size = self.tell()
        self._buffer.truncate(size)

    def tell(self) -> int:
        return self._buffer.tell()

    def getvalue(self) -> str:
        """Get the current value of the buffer."""
        return self._buffer.getvalue()
    
    def toString(self) -> str:

        """Get the current value of the buffer as a string."""
        return str(self._buffer.getvalue())

    def clear(self) -> Self:
        """Clear the buffer."""
        self._buffer.truncate(0)
        self._buffer.seek(0)
        return self