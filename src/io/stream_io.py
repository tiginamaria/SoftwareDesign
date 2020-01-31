class StreamIO:
    """ Class to store transitional result for commands in pipe. """

    def __init__(self):
        """ Initialise io stream. """
        self.stream = None

    def write(self, string: str):
        """ Write given string into stream.
        :param string: string to store
        """
        self.stream = string

    def read(self):
        """ Read string from stream.
        :return: stored string
        """
        return self.stream

    def clear(self):
        """ Clear stream. """
        self.stream = None
