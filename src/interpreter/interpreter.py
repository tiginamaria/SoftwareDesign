from src.interpreter.commands import Command
from src.io.stream_io import StreamIO
from src.runnable import Runnable


class Interpreter(Runnable):

    def __init__(self, env):
        self.env = env

    def run(self, input):
        return self.interpret(input)

    def interpret(self, commands: [Command]):
        input = StreamIO()
        output = StreamIO()
        code = 0
        for command in commands:
            code = command.execute(self.env, input, output)
            input.clear()
            input, output = output, input
        out = input.read()[0] if len(input.read()) > 0 else None
        return code, out
