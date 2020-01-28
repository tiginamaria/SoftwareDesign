from src.parser.commands.command import Command


class Echo(Command):

    def execute(self, env, stream):
        print('echo', stream.read())
        if self.args:
            stream.write(" ".join(self.args))
        else:
            stream.write("")
        return 0
