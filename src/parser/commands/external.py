from src.parser.commands.command import Command


class External(Command):

    def __init__(self, args, name):
        super().__init__(args)
        self.name = name

    def execute(self, env, stream):
        print(stream.read())
        return 0
