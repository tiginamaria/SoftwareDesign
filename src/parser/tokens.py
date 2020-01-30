import re

from pypeg2 import some, maybe_some, name, ignore


class Token:

    def __init__(self, content=None):
        self.content = content


class Blank(Token):
    grammar = maybe_some(re.compile(r"\s+"))


class AssignmentToken(Token):
    Variable = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    Value = re.compile(r"('[^']*'|\"[^\"]*\"|[^\"'|\s]+)*")

    grammar = Variable, "=", Value


class DoubleQuotesToken(Token):
    grammar = "\"", re.compile(r"[^\"]*"), "\""

    def to_string(self):
        return "\"{}\"".format(self.content)


class SingleQuotesToken(Token):
    grammar = "\'", re.compile(r"[^']*"), "\'"

    def to_string(self):
        return "'{}'".format(self.content)


class NoQuotesToken(Token):
    grammar = re.compile(r"[^\"|'\s]+")

    def to_string(self):
        return self.content


class ArgumentToken(Token):
    grammar = some([DoubleQuotesToken, SingleQuotesToken, NoQuotesToken])

    def get_content(self):
        return "".join(map(lambda token: token.content, self.content))

    def to_string(self):
        return "".join(map(lambda token: token.to_string(), self.content))


class CommandToken(Token):
    grammar = name(), maybe_some(ignore(Blank), ArgumentToken)


class PipeToken(Token):
    grammar = CommandToken, maybe_some(ignore(Blank), "|", ignore(Blank), CommandToken)
