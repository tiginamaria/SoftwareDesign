from src.environment import Environment
from src.interpreter.commands import ExecutableCommand, ExecutableCommandException
from src.io.stream_io import StreamIO
from src.pipeline import Runnable


class InterpreterException(Exception):
    """ Exception raise in case of wrong interpreting process. """

    def __init__(self, message):
        super(InterpreterException, self).__init__("interpreter: {}".format(message))


class Interpreter(Runnable):
    """ Class Interpreter for Commands"""

    def __init__(self, env: Environment):
        "Initialise environment for interpreter. """
        self.env = env

    def run(self, input: [ExecutableCommand]):
        """ Run interpreter on the given input. """
        return self.interpret(input)

    def interpret(self, commands: [ExecutableCommand]):
        """ Execute given list of commands as a pipe. The output of previous command is given to the next command input.
        :param commands: list of commands to execute
        :return: pair of return code and last command output
        :raise: InterpreterException in case of inappropriate command execution
        """
        input = StreamIO()
        output = StreamIO()
        code = 0
        for command in commands:
            try:
                code = command.execute(self.env, input, output)
            except ExecutableCommandException as e:
                raise InterpreterException(e)
            if code != 0:
                return code, input.read()
            input.clear()
            input, output = output, input
        return code, input.read()
