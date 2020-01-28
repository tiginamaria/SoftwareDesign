from src.io.stream import IOStream
from src.parser.commands.command import Command
from src.runnable import Runnable


class Interpreter(Runnable):

    def __init__(self, env):
        self.env = env

    def interpret(self, commands: [Command]):
        stream = IOStream()
        for command in commands:
            code = command.execute(self.env, stream)
        print("".join(stream.read()))

    def run(self, input):
        self.interpret(input)
