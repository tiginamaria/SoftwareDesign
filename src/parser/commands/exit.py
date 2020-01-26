from src.parser.commands.command import Command


class Exit(Command):

    def execute(self, env, input, output):
        print(input)
