import re

from pypeg2 import maybe_some

from src.environment import Environment


class SubstitutionToken:
    """ Abstract class for all substituter tokens. """

    def __init__(self, content=None):
        """ Initialize content of substituter token. """
        self.content = content

    def substitute(self, env: Environment):
        """ Process substitution in content of token. """
        pass

    def to_string(self):
        """ Convert token to string. """
        return self.content


class VariableSubstitution(SubstitutionToken):
    """ Class for variable substitution expression token. """

    grammar = "$", re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    def substitute(self, env):
        self.content = env[self.content]


class SingleQuotes(SubstitutionToken):
    """ Class for single quotes substituter token. """

    grammar = re.compile(r"'[^']*'")


class StringNoDoubleQuotes(SubstitutionToken):
    """ Class for substituter token without double quotes. """

    grammar = re.compile(r"[^$\"]+")


class DoubleQuotes(SubstitutionToken):
    """ Class for double quotes substituter token. """

    grammar = "\"", maybe_some([StringNoDoubleQuotes, VariableSubstitution]), "\""

    def substitute(self, env):
        if self.content:
            for token in self.content:
                token.substitute(env)

    def to_string(self):
        in_quotes = [token.to_string() for token in self.content] if self.content else []
        return "\"" + "".join(in_quotes) + "\""


class NoQuotes(SubstitutionToken):
    """ Class for substituter token without any quotes. """

    grammar = re.compile(r"[^$'\"]+")
