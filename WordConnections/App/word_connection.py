
class WordConnection:
    def __init__(self,name,connection):
        self.name = name
        self.connection = connection
        
    def __str__(self):
        return f"WordConnection(name={self.name}, connection={self.connection})"