class Synonym:
    def __init__(self, short, command):
        self._short = short
        self._command = command
        
    def getCommand(self):
        return self._command