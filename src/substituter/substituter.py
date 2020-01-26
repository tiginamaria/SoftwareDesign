from pypeg2 import some, parse, maybe_some

from src.runnable import Runnable
from src.substituter.tokens.blank import Blank
from src.substituter.tokens.double_quotes import DoubleQuotes
from src.substituter.tokens.no_quotes import NoQuotes
from src.substituter.tokens.single_quotes import SingleQuotes


class Substituter(Runnable):

    def __init__(self, env):
        self.env = env

    def substitute(self, input: str) -> str:
        tokens = parse(input, some(maybe_some(Blank), [SingleQuotes, DoubleQuotes, NoQuotes]), whitespace="")
        for token in tokens:
            token.substitute(self.env)
        return "".join(list(map(lambda token: token.to_string(), tokens)))

    def run(self, input):
        return self.substitute(input)
