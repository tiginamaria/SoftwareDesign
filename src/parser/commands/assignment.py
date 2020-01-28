from src.parser.commands.command import Command


class Assignment(Command):

    def execute(self, env, stream):
        variable, value = stream.read()
        env.set(variable, value)
        return 0
