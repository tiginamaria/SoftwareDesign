from src.interpreter.commands import Command, Cat, Echo, Exit, Pwd, Wc, External, Assignment
from src.parser.tokens import ArgumentToken


class CommandFactory:
    """ Class implements pattern factory to create executable commands from parser tokens. """

    def __init__(self):
        """ Initialize functions to create standard commands. """
        self.commands_creators = {'cat': self.create_cat,
                                  'echo': self.create_echo,
                                  'exit': self.create_exit,
                                  'pwd': self.create_pwd,
                                  'wc': self.create_wc}

    def create(self, name: str, args: [ArgumentToken]) -> Command:
        """ Create command with given name and arguments.
        :param name: command name
        :param args: command's arguments
        :return: created command object
        """
        create_command = self.commands_creators.get(name, lambda a: self.create_external(name, a))
        return create_command(args)

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

    def create_cat(self, arg_tokens) -> Cat:
        """ Create cat command. """
        args = self.create_args(arg_tokens)
        return Cat(args)

    def create_echo(self, arg_tokens) -> Echo:
        """ Create echo command. """
        args = self.create_args(arg_tokens)
        return Echo(args)

    def create_exit(self, arg_tokens) -> Exit:
        """ Create exit command. """
        args = self.create_args(arg_tokens)
        return Exit(args)

    def create_pwd(self, arg_tokens) -> Pwd:
        """ Create pwd command. """
        args = self.create_args(arg_tokens)
        return Pwd(args)

    def create_wc(self, arg_tokens) -> Wc:
        """ Create wc command. """
        args = self.create_args(arg_tokens)
        return Wc(args)

    def create_external(self, name, arg_tokens) -> External:
        """ Create external command. """
        args = self.create_args(arg_tokens, lambda arg: arg.to_string())
        return External(name, args)

    def create_assignment(self, args) -> Assignment:
        """ Create assignment command. """
        args = [args[0]] + self.create_args([args[1]])
        return Assignment(args)
