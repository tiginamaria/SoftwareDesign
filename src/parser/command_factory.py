from src.interpreter.commands import ExecutableCommand, Cat, Echo, Exit, Pwd, Wc, External, Assignment
from src.parser.tokens import ArgumentToken


class CommandFactory:
    """ Class implements pattern factory to create executable commands from parser tokens. """

    def __init__(self):
        """ Initialize functions to create standard commands. """
        self.commands = {'cat': Cat,
                         'echo': Echo,
                         'exit': Exit,
                         'pwd': Pwd,
                         'wc': Wc}

    def create(self, name: str, arg_tokens: [ArgumentToken]) -> ExecutableCommand:
        """ Create command with given name and arguments.
        :param name: command name
        :param arg_tokens: command's arguments
        :return: created command object
        """
        command = self.commands.get(name, External)
        if command == External:
            return self.create_external(name, arg_tokens)
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
