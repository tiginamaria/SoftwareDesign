from src.parser.tokens.terminals import Variable, Argument
from src.parser.tokens.token import Token


class AssignmentToken(Token):

    grammar = Variable, "=", Argument

