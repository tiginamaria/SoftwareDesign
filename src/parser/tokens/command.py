import re

from pypeg2 import name, some, maybe_some, ignore

from src.parser.tokens.blank import Blank
from src.parser.tokens.token import Token


class DoubleQuotes(Token):
    grammar = "\"", re.compile(r"[^\"]*"), "\""


class SingleQuotes(Token):
    grammar = "\'", re.compile(r"[^']*"), "\'"


class NoQuotes(Token):
    grammar = re.compile(r"[^\"|'\s]+")


class Argument(Token):
    grammar = some([DoubleQuotes, SingleQuotes, NoQuotes])


class CommandToken(Token):
    grammar = name(), maybe_some(ignore(Blank), Argument)
