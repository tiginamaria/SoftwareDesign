from src.parser.commands.command import Command


class Pwd(Command):



    def execute(self, env, input, output):
        print(input)
