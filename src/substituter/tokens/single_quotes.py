import re
from src.substituter.tokens.substitution_token import SubstitutionToken


class SingleQuotes(SubstitutionToken):
    grammar = re.compile(r"'[^']*'")
