from pypeg2 import maybe_some, ignore

from src.parser.tokens.blank import Blank
from src.parser.tokens.command import CommandToken
from src.parser.tokens.token import Token


class PipeToken(Token):
    grammar = CommandToken, maybe_some(ignore(maybe_some(Blank)), "|", ignore(maybe_some(Blank)), CommandToken)
