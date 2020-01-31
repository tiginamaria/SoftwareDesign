class Environment:
    """ Class to store environment variables. """

    def __init__(self, env: dict):
        "Initialise environment. """
        self.env = env

    def __setitem__(self, key: str, value: str):
        """ Add variable to environment.
        :param key: variable name
        :param value: variable value
        """
        self.env[key] = value

    def __getitem__(self, key):
        """ Get variable from environment.
        :param key: name of variable
        :return: value of given variable if exists or empty string
        """
        return self.env.get(key, "")
