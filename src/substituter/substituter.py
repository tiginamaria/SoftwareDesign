from pypeg2 import parse, maybe_some

from src.pipeline import Runnable
from src.substituter.tokens import VariableSubstitution, DoubleQuotes, SingleQuotes, NoQuotes


class SubstituterException(Exception):
    """ Exception raise in case of wrong substituting process. """

    def __init__(self, message):
        super(SubstituterException, self).__init__("substitutor: {}".format(message))


class Substituter(Runnable):
    """ Class implements substitution of variable to values environment. """

    def __init__(self, env):
        "Initialise environment for substituter. """
        self.env = env

    def run(self, input: str) -> str:
        """ Run substituter on given input. """
        return self.substitute(input)

    def substitute(self, input: str) -> str:
        """ Substitute variables in string with values from environment.
        :param input: string to substitute variables in.
        :return: string with
        :raise: SubstituterException in case of inappropriate substitution
        """
        try:
            tokens = parse(input, maybe_some([NoQuotes, SingleQuotes, DoubleQuotes, VariableSubstitution]),
                           whitespace="")
        except (SyntaxError, ValueError, TypeError):
            raise SubstituterException("can not process substitution")
        for token in tokens:
            token.substitute(self.env)
        return "".join(list(map(lambda token: token.to_string(), tokens)))
