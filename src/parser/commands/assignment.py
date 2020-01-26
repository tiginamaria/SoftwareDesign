from src.parser.commands.command import Command


class Assignment(Command):

    def execute(self, env, input, output):
        variable, value = input.read()
        env.set(variable, value)
        return 0
