from pypeg2 import parse

from src.parser.command_factory import CommandFactory
from src.parser.tokens.assignment import AssignmentToken
from src.parser.tokens.pipe import PipeToken
from src.runnable import Runnable


class Parser(Runnable):

    def __init__(self):
        self.factory = CommandFactory()

    def parse(self, input):
        token = parse(input, [AssignmentToken, PipeToken])
        if isinstance(token, AssignmentToken):
            return [self.factory.create('assignment', token.args)]
        elif isinstance(token, PipeToken):
            return [self.factory.create(command.name, command.args) for command in token.args]
        else:
            raise IOError("No such command!")

    def run(self, input):
        return self.parse(input)
