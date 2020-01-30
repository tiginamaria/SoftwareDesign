import os
import subprocess

from src.environment import Environment
from src.io.stream_io import StreamIO


class CommandException(Exception):
    pass


class Command:
    """ Base abstract class to emulate bash commands."""

    def __init__(self, args=None):
        self.args = args

    def execute(self, env: Environment, input: StreamIO, output: StreamIO) -> int:
        """ Execute command.
        :param env: environment
        :param input: stream to read input from
        :param output: stream to write output to
        :return: code: return code (0) - successful execution to continue, (-1) - program should be interrupted
        :raise: CommandException: in case of improper execution
        """
        pass


class Assignment(Command):
    """ Class emulate bash assignment - add new variable to environment."""

    def execute(self, env, input, output):
        """ Execute assignment command: add new variable to environment. """

        assert self.args == 2, "illegal argument exception, expected two arguments," \
                               " got {}: {}".format(len(self.args), self.args)
        variable, value = self.args
        env[variable] = value
        return 0


class Cat(Command):
    """ Class emulate bash command cat - concatenate files and print on the standard output. """

    def execute(self, env, input, output):
        result = ""
        if self.args:
            try:
                for file in self.args:
                    with open(file, "r") as f:
                        result += f.read()
            except IOError as e:
                raise CommandException('cat: {}'.format(e))
        else:
            result = "".join(input.read())
        output.write(result)
        return 0


class Echo(Command):
    """ Class emulate bash command cat - concatenate files and print on the standard output. """

    def execute(self, env, input, output):
        if self.args:
            output.write(" ".join(self.args))
        else:
            output.write("")
        return 0


class Exit(Command):
    """ Class emulate bash command echo - display a line of text. """

    def execute(self, env, input, output):
        return -1


class Pwd(Command):

    def execute(self, env, input, output):
        output.write(os.getcwd())
        return 0


class Wc(Command):
    """ Class for bash command wc - print newline, word, and byte counts for each file """

    def str_statistics(self, text):
        lines = len(text.split('\n'))
        words = len(text.split())
        bytes = len(text.encode('utf-8'))
        return '{}  {}  {}'.format(lines, words, bytes)

    def file_statistics(self, file):
        with open(file, 'r') as f:
            content = f.read()
            counts = self.str_statistics(content)
        return '{}  {}\n'.format(counts, file)

    def execute(self, env, input, output):
        result = ""
        if self.args:
            for arg in self.args:
                try:
                    result += self.file_statistics(arg)
                except IOError as e:
                    CommandException('wc : {}'.format(e))
        else:
            if len(input.read()) == 0:
                return 1
            result = self.str_statistics(input.read()[0])
        output.write(result)
        return 0


class External(Command):

    def __init__(self, name, args):
        super().__init__(args)
        self.name = name

    def execute(self, env, input, output):
        encoded_input = " ".join(input.read()).encode() if input else None
        try:
            if not self.args:
                self.args = []
            result = subprocess.run([self.name] + self.args, check=True, input=encoded_input,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            raise CommandException(error.stderr.decode())
        except FileNotFoundError:
            raise CommandException('{}: command not found'.format(self.name))
        output.write(result.stdout.decode())
        return 0
