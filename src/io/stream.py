
class IOStream:

    def __init__(self):
        self.stream = []

    def write(self, values):
        self.stream = values

    def read(self):
        return self.stream

    def clear(self):
        self.stream = []
