from src.parser.commands.command import Command


class Echo(Command):
    def execute(self, env, input, output):
        print(input)
