from io import StringIO
from ..languages import Language
 
class StringWriter:
    def __init__(self, language: Language):
        self.Language = language
        self._buffer = StringIO()
        self.I = ' ' * 3
        self.N = 0

    def newline(self) -> str:
        return "\n"

    def o(self) -> StringIO:
        """Open."""
        
        self.write("{")
        self.Inc()
        return self
    
    def n(self) -> StringIO:
        self.write(self.newline())
        return self
    

    def Inc(self, n=1) -> StringIO:
        self.N = self.N + n 

    def Dec(self, n = 1) -> StringIO:
        self.N = self.N - n 
    
    def c(self) -> StringIO:
        """Close."""
        self.Dec()
        self.write("}")
        self.write(self.newline())
        return self
    
    def f(self) -> StringIO:
        """Open Function."""
        self.write("function")
        return self

    def write(self, text: str) -> None:
        """Write text to the buffer."""
        self._buffer.write(self.I * self.N)
        self._buffer.write(text)
        return self
    
    def w(self, text: str) -> None: 
        return self.write(text)
    
    def writeline(self, text: str) -> None:
        """Write text to the buffer."""
        self.write(text)
        self.write(self.newline())
        return self
    
    def ret(self) -> None:
        return self.writeline("")
    
    def wln(self, text: str) -> None:
        return self.writeline(text)

    def flush(self) -> None:
        """Flush the buffer."""
        self._buffer.flush()
        return self

    def seek(self, offset: int, whence: int = 0) -> None:
        """Move the cursor to a specific position in the buffer."""
        self._buffer.seek(offset, whence)
        return self

    def read(self, size: int = -1) -> str:
        """Read a specified number of characters from the buffer."""
        return self._buffer.read(size)
    
    def readline(self) -> str:
        """Read a single line from the buffer."""
        return self._buffer.readline()
    
    def readlines(self) -> list:
        """Read all lines from the buffer."""
        return self._buffer.readlines()
    
    def truncate(self, size: int = None) -> None:
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

    def clear(self) -> None:
        """Clear the buffer."""
        self._buffer.truncate(0)
        self._buffer.seek(0)
        return self