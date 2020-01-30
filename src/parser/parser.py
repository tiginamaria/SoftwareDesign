from pypeg2 import parse

from src.interpreter.commands import Command, Cat, Assignment, Echo, Exit, Pwd, Wc, External
from src.parser.tokens import AssignmentToken, PipeToken, ArgumentToken
from src.runnable import Runnable


class Parser(Runnable):

    def __init__(self):
        self.standard_commands = {'cat': self.parse_cat,
                                  'echo': self.parse_echo,
                                  'exit': self.parse_exit,
                                  'pwd': self.parse_pwd,
                                  'wc': self.parse_wc}

    def run(self, input: str):
        return self.parse(input)

    def parse(self, input: str) -> [Command]:
        token = parse(input, [AssignmentToken, PipeToken], whitespace="")
        if isinstance(token, AssignmentToken):
            return [self.parse_assignment(token.content)]
        elif isinstance(token, PipeToken):
            return [self.parse_command(command.name, command.content) for command in token.content]
        else:
            raise IOError("{}: not found".format(input))

    def parse_args(self, arg_tokens: [ArgumentToken], to_str=lambda arg: arg.get_content()) -> [str]:
        if arg_tokens is None:
            return None
        args = []
        for arg_token in arg_tokens:
            args.append(to_str(arg_token))
        return args

    def parse_cat(self, arg_tokens) -> Cat:
        args = self.parse_args(arg_tokens)
        return Cat(args)

    def parse_echo(self, arg_tokens) -> Echo:
        args = self.parse_args(arg_tokens)
        return Echo(args)

    def parse_exit(self, arg_tokens) -> Exit:
        args = self.parse_args(arg_tokens)
        return Exit(args)

    def parse_pwd(self, arg_tokens) -> Pwd:
        args = self.parse_args(arg_tokens)
        return Pwd(args)

    def parse_wc(self, arg_tokens) -> Wc:
        args = self.parse_args(arg_tokens)
        return Wc(args)

    def parse_external(self, name, arg_tokens) -> External:
        args = self.parse_args(arg_tokens, lambda arg: arg.to_string())
        return External(name, args)

    def parse_assignment(self, args) -> Assignment:
        args = self.parse_args(args)
        return Assignment(args)

    def parse_command(self, name, args) -> Command:
        parser = self.standard_commands.get(name, lambda a: self.parse_external(name, a))
        return parser(args)
