import os

from src.environment import Environment
from src.interpreter.interpreter import Interpreter, InterpreterException
from src.parser.command_factory import ArgumentParserException
from src.parser.parser import Parser, ParserException
from src.pipeline import Pipeline
from src.substituter.substituter import Substituter, SubstituterException


class CLI:
    """ Command-line interface for bash single line commands. """

    def __init__(self):
        "Initialise environment and interpretation pipeline for cli. """
        self.env = Environment(os.environ)
        self.pipeline = Pipeline()
        self.pipeline.add([Substituter(self.env), Parser(), Interpreter(self.env)])

    def run(self, input: str) -> (int, str):
        """ Run substituter, parser, interpreter one by one.
        :param input: input string to process
        :return: cli result
        """
        return self.pipeline.run(input)

    def start(self):
        """ Read and process command from stdio. """
        while True:
            inp = input()
            try:
                code, out = self.run(inp)
            except (InterpreterException, ParserException, SubstituterException, ArgumentParserException) as e:
                code, out = 1, e
            if code == -1:
                break
            if out is not None:
                print(out)
