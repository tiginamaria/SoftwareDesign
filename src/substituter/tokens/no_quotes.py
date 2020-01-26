import re

from pypeg2 import some, maybe_some

from src.substituter.tokens.blank import Blank
from src.substituter.tokens.substitution_token import SubstitutionToken
from src.substituter.tokens.variable_substitution import VariableSubstitution


class NoQuotesAndSubstitution(SubstitutionToken):
    grammar = re.compile(r"[^$'\"\s]+")


class NoQuotes(SubstitutionToken):
    grammar = some(maybe_some(Blank), [NoQuotesAndSubstitution, VariableSubstitution])

    def substitute(self, env):
        for token in self.content:
            token.substitute(env)

    def to_string(self):
        return "".join(list(map(lambda token: str(token.to_string()), self.content)))
