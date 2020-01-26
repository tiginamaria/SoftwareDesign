from src.environment import Environment


class SubstitutionToken:
    def __init__(self, content):
        self.content = content

    def substitute(self, env: Environment):
        pass

    def to_string(self):
        return self.content
