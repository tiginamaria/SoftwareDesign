import os

from src.parser.commands.command import Command


class Pwd(Command):

    def execute(self, env, stream):
        stream.write(os.getcwd())
        return 0
