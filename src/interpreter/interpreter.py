from src.io.stream import IOStream
from src.parser.commands.command import Command
from src.runnable import Runnable


class Interpreter(Runnable):

    def init__(self, env):
        self.env = env

    def interpret(self, commands: [Command]):
        input = IOStream()
        output = IOStream()
        for command in commands:
            code = command.execute(self.env, input, output)
            input.clear()
            input, output = output, input

    def run(self, input):
        self.interpret(input)
