import re

from src.parser.tokens.token import Token


class AssignmentToken(Token):
    Variable = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")

    Value = re.compile(r"('[^']*'|\"[^\"]*\"|[^\"'|\s]+)*")

    grammar = Variable, "=", Value
