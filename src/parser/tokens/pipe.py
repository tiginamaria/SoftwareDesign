from pypeg2 import maybe_some, blank

from src.parser.tokens.command import CommandToken
from src.parser.tokens.token import Token


class PipeToken(Token):

    grammar = CommandToken, maybe_some(blank, "|", blank, CommandToken)
