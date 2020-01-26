import re

Argument = re.compile(r"'[^'\s]*'|\"[^\"\s]*\"|[^\"'|\s]+")

Variable = re.compile(r"[_a-zA-Z][_a-zA-Z0-9]*")
