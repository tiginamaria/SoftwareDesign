import os

from src.environment import Environment
from src.interpreter.interpreter import Interpreter
from src.parser.parser import Parser
from src.pipeline import Pipeline
from src.substituter.substituter import Substituter


class CLI:

    def __init__(self):
        self.env = Environment(os.environ)
        self.pipeline = Pipeline()
        self.pipeline.add([Substituter(self.env), Parser(), Interpreter(self.env)])

    def run(self, input):
        return self.pipeline.run(input)


if __name__ == "__main__":
    cli = CLI()
    while True:
        inp = input()
        print(inp)
        code = cli.run(inp)
        if code == -1:
            break
