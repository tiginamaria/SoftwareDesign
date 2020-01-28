from src.parser.commands.command import Command


class Cat(Command):

    def execute(self, env, stream):
        if self.args:
            files = self.args
        else:
            files = stream.read()
        output = ""
        for file in files:
            with open(file, "r") as f:
                output += f.read()
        stream.write(output)
        return 0
