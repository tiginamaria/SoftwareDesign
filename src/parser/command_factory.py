import argparse

from src.interpreter.commands import ExecutableCommand, Cat, Echo, Exit, Pwd, Wc, Grep, External, Assignment
from src.parser.tokens import ArgumentToken


class ArgumentParserException(Exception):
    """ Exception raise in case of wrong argument parsing process. """

    def __init__(self, message):
        super(ArgumentParserException, self).__init__("parser: {}".format(message))


class ArgumentParser(argparse.ArgumentParser):
    """ Class to parse flags. """

    def error(self, message):
        raise ArgumentParserException(message)


class CommandFactory:
    """ Class implements pattern factory to create executable commands from parser tokens. """

    def __init__(self):
        """ Initialize functions to create standard commands. """
        self.commands = {'cat': Cat,
                         'echo': Echo,
                         'exit': Exit,
                         'pwd': Pwd,
                         'wc': Wc,
                         'grep': Grep}

    def create(self, name: str, arg_tokens: [ArgumentToken]) -> ExecutableCommand:
        """ Create command with given name and arguments.
        :param name: command name
        :param arg_tokens: command's arguments
        :return: created command object
        """
        command = self.commands.get(name, External)
        if command == External:
            return self.create_external(name, arg_tokens)
        if command == Grep:
            return self.create_grep(arg_tokens)
        return self.create_base(command, arg_tokens)

    @staticmethod
    def create_args(arg_tokens: [ArgumentToken], to_str=lambda arg: arg.get_content()) -> [str]:
        """ Map argument's tokens to string command arguments.
        :param arg_tokens: argument's tokens
        :param to_str: function to create string argument from argument token
        :return: list of string arguments
        """
        if arg_tokens is None:
            return None
        args = []
        for arg_token in arg_tokens:
            args.append(to_str(arg_token))
        return args

    def create_assignment(self, args) -> Assignment:
        """ Create assignment command. """
        args = [args[0]] + self.create_args([args[1]])
        return Assignment(args)

    def create_base(self, command, arg_tokens) -> ExecutableCommand:
        """ Create assignment command. """
        args = self.create_args(arg_tokens)
        return command(args)

    def create_external(self, name, arg_tokens) -> ExecutableCommand:
        """ Create assignment command. """
        args = self.create_args(arg_tokens, lambda arg: arg.to_string())
        return External(name, args)

    def create_grep(self, arg_tokens) -> ExecutableCommand:
        """ Create grep command. """
        parser = ArgumentParser()
        parser.add_argument("-i", action='store_true',
                            help="Ignore case distinctions.")
        parser.add_argument("-w", action='store_true',
                            help="Select only those lines containing matches that form whole words.")
        parser.add_argument("-A", type=int, default=1,
                            help="Print NUM lines of trailing context after matching lines.")
        parser.add_argument('pattern', type=str, help='Pattern to grep')
        parser.add_argument('files', type=str, nargs='*', help='File(s) to grep')
        args = self.create_args(arg_tokens)
        flags = parser.parse_args(args)
        return Grep(flags)
