
from src.parser.commands.command import Command


class Cat(Command):

    def execute(self, env, input, output):
        print(input)
