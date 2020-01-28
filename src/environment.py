class Environment:

    def __init__(self, env):
        self.env = env

    def set(self, key, value):
        self.env[key] = value

    def get(self, key):
        return self.env.get(key, "")
