from src.parser.commands.command import Command


class Wc(Command):

    def execute(self, env, input, output):
        print(input)
