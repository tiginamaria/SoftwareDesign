class Environment:

    def __init__(self, env):
        self.env = env

    def __setitem__(self, key, value):
        self.env[key] = value

    def __getitem__(self, key):
        return self.env.get(key, "")
