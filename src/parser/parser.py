from pypeg2 import parse

from src.parser.command_factory import CommandFactory
from src.parser.commands.assignment import Assignment
from src.parser.tokens.assignment import AssignmentToken
from src.parser.tokens.command import Argument
from src.parser.tokens.pipe import PipeToken
from src.runnable import Runnable


class Parser(Runnable):

    def __init__(self):
        self.factory = CommandFactory()

    def parse_args(self, arg_tokens: [Argument]):
        if arg_tokens is None:
            return None
        args = []
        for arg_token in arg_tokens:
            args.append("".join(map(lambda quote_token: quote_token.content, arg_token.content)))
        return args

    def parse(self, input):
        token = parse(input, [AssignmentToken, PipeToken], whitespace="")
        if isinstance(token, AssignmentToken):
            return [Assignment(token.content)]
        elif isinstance(token, PipeToken):
            return [self.factory.create(command.name, self.parse_args(command.content)) for command in token.content]
        else:
            raise IOError("{}: not found".format(input))

    def run(self, input):
        return self.parse(input)
