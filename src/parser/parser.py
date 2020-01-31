from pypeg2 import parse

from src.interpreter.commands import Command
from src.parser.command_factory import CommandFactory
from src.parser.tokens import AssignmentToken, PipeToken
from src.pipeline import Runnable


class ParserException(Exception):
    """ Exception raise in case of wrong parsing process. """

    def __init__(self, message):
        super(ParserException, self).__init__("parser: {}".format(message))


class Parser(Runnable):

    def __init__(self):
        """ Initialize command factory for all supported commands. """
        self.command_factory = CommandFactory()

    def run(self, input: str) -> [Command]:
        """ Run parser on given inputz. """
        return self.parse(input)

    def parse(self, input: str) -> [Command]:
        """ Parse input string to list of executable commands.
        :param input: string to parse
        :return: list of commands parsed from input string
        :raise: ParserException if input string can not be parsed to command
        """
        try:
            token = parse(input, [AssignmentToken, PipeToken], whitespace="")
        except (SyntaxError, ValueError, TypeError):
            raise ParserException("command not found")
        if isinstance(token, AssignmentToken):
            return [self.command_factory.create_assignment(token.content)]
        elif isinstance(token, PipeToken):
            return [self.command_factory.create(command.name, command.content) for command in token.content]
