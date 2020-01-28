class IOStream:

    def __init__(self):
        self.stream = []

    def write(self, values):
        self.stream = []
        self.stream.append(values)

    def read(self):
        return self.stream

    def append(self, values):
        self.stream.append(values)

    def clear(self):
        self.stream = ""
