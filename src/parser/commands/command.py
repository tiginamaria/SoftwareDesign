from src.environment import Environment
from src.io.stream import IOStream


class Command:

    def __init__(self, args=None):
        self.args = args

    def execute(self, env: Environment, input: IOStream, output: IOStream):
        pass