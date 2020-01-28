import re

from src.substituter.tokens.substitution_token import SubstitutionToken


class Blank(SubstitutionToken):
    grammar = re.compile(r"\s+")
