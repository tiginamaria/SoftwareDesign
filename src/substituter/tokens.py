import re

from pypeg2 import maybe_some

from src.environment import Environment


class SubstitutionToken:
    def __init__(self, content):
        self.content = content

    def substitute(self, env: Environment):
        pass

    def to_string(self):
        return self.content


class VariableSubstitution(SubstitutionToken):
    grammar = "$", re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    def substitute(self, env):
        self.content = env[self.content]

    def to_string(self):
        return self.content


class SingleQuotes(SubstitutionToken):
    grammar = re.compile(r"'[^']*'")


class StringNoDoubleQuotes(SubstitutionToken):
    grammar = re.compile(r"[^$\"]+")


class DoubleQuotes(SubstitutionToken):
    grammar = "\"", maybe_some([StringNoDoubleQuotes, VariableSubstitution]), "\""

    def substitute(self, env):
        for token in self.content:
            token.substitute(env)

    def to_string(self):
        return "\"" + "".join(list(map(lambda token: str(token.to_string()), self.content))) + "\""


class NoQuotes(SubstitutionToken):
    grammar = re.compile(r"[^$'\"]+")
