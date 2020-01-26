import re

from pypeg2 import maybe_some

from src.substituter.tokens.blank import Blank
from src.substituter.tokens.substitution_token import SubstitutionToken
from src.substituter.tokens.variable_substitution import VariableSubstitution


class StringNoDoubleQuotes(SubstitutionToken):
    grammar = re.compile(r"[^$\"]+")


class DoubleQuotes(SubstitutionToken):
    grammar = "\"", maybe_some(maybe_some(Blank), [StringNoDoubleQuotes, VariableSubstitution]), "\""

    def substitute(self, env):
        for token in self.content:
            token.substitute(env)

    def to_string(self):
        return "\"" + "".join(list(map(lambda token: str(token.to_string()), self.content))) + "\""
