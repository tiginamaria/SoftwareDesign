import re

from src.substituter.tokens.substitution_token import SubstitutionToken


class Variable(SubstitutionToken):
    grammar = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    def substitute(self, env):
        self.content = env.get(self.content)


class VariableSubstitution(SubstitutionToken):
    grammar = "$", Variable

    def substitute(self, env):
        self.content.substitute(env)

    def to_string(self):
        return self.content.to_string()
