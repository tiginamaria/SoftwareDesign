from pypeg2 import parse, maybe_some

from src.runnable import Runnable
from src.substituter.tokens import VariableSubstitution, DoubleQuotes, SingleQuotes, NoQuotes


class Substituter(Runnable):

    def __init__(self, env):
        self.env = env

    def run(self, input):
        return self.substitute(input)

    def substitute(self, input: str) -> str:
        tokens = parse(input, maybe_some([NoQuotes, SingleQuotes, DoubleQuotes, VariableSubstitution]), whitespace="")
        for token in tokens:
            token.substitute(self.env)
        return "".join(list(map(lambda token: token.to_string(), tokens)))
