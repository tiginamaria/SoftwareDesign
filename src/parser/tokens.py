import re

from pypeg2 import some, maybe_some, name, ignore


class ParserToken:
    """ Abstract class for all parser tokens. """

    def __init__(self, content=None):
        """ Initialize parsed content of token. """
        self.content = content


class Blank(ParserToken):
    """ Class for blank symbols parser token. """

    grammar = maybe_some(re.compile(r"\s+"))


class DoubleQuotesToken(ParserToken):
    """ Class for double quotes parser token. """

    grammar = "\"", re.compile(r"[^\"]*"), "\""

    def to_string(self):
        return "\"{}\"".format(self.content)


class SingleQuotesToken(ParserToken):
    """ Class for single quotes parser token. """

    grammar = "\'", re.compile(r"[^']*"), "\'"

    def to_string(self):
        return "'{}'".format(self.content)


class NoQuotesToken(ParserToken):
    """ Class for parser token without any quotes. """

    grammar = re.compile(r"[^\"|'\s]+")

    def to_string(self):
        return self.content


class ArgumentToken(ParserToken):
    """ Class for parser argument token. """

    grammar = some([DoubleQuotesToken, SingleQuotesToken, NoQuotesToken])

    def get_content(self):
        """ Get argument with removed quotes. """
        return "".join(map(lambda token: token.content, self.content))

    def to_string(self):
        """ Get argument with quotes. """
        return "".join(map(lambda token: token.to_string(), self.content))


class CommandToken(ParserToken):
    """ Class for command expression parser token. """

    grammar = name(), maybe_some(ignore(Blank), ArgumentToken)


class PipeToken(ParserToken):
    """ Class for pipe expression parser token. """

    grammar = ignore(Blank), CommandToken, maybe_some(ignore(Blank), "|", ignore(Blank), CommandToken), ignore(Blank)


class AssignmentToken(ParserToken):
    """ Class for assignment parser token. """

    Variable = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    grammar = ignore(Blank), Variable, "=", ArgumentToken, ignore(Blank)
