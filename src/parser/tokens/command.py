from pypeg2 import name, blank, maybe_some

from src.parser.tokens.terminals import Argument
from src.parser.tokens.token import Token


class CommandToken(Token):

    grammar = name(), maybe_some(blank, Argument)
