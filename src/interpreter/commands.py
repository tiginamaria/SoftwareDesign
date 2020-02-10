import os
import re
import subprocess

from src.environment import Environment
from src.io.stream_io import StreamIO


class CommandException(Exception):
    """ Exception raises in case of wrong command behaviour. """

    def __init__(self, name, message):
        super(CommandException, self).__init__("{}: {}".format(name, message))


class Command:
    """ Base abstract class to emulate bash commands."""

    def __init__(self, args=None):
        """ Initialise arguments. """
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
                raise CommandException('cat', e)
        else:
            result = input.read()
        output.write(result)
        return 0


class Echo(Command):
    """" Class emulate bash command echo - display a line of text. """

    def execute(self, env, input, output):
        if self.args:
            output.write(" ".join(self.args))
        else:
            output.write("")
        return 0


class Exit(Command):
    """ Class emulate bash command exit - cause normal process termination. """

    def execute(self, env, input, output):
        return -1


class Pwd(Command):
    """ Class for bash command pwd - print name of current/working directory. """

    def execute(self, env, input, output):
        output.write(os.getcwd())
        return 0


class Grep(Command):
    """ Class for bash command grep - print lines matching a pattern. """

    def search(self, pattern, line):
        if self.args.w:
            pattern = "\\b" + pattern + "\\b"
        if self.args.i:
            return re.search(pattern, line, re.IGNORECASE)
        return re.search(pattern, line)

    def grep_file(self, text):
        result = []
        matched = -1
        for n, line in enumerate(text):
            if n > matched:
                if self.search(self.args.pattern, line):
                    result.append(line)
                    matched = n + self.args.A - 1
            else:
                result.append(line)
        return ''.join(result)

    def execute(self, env, input, output):
        result = []
        if len(self.args.files) > 0:
            for file in self.args.files:
                try:
                    with open(file) as f:
                        matched_lines = self.grep_file(f)
                    if matched_lines:
                        result.append(matched_lines)
                except IOError as e:
                    raise CommandException('grep', e)
            output.write(''.join(result))
        elif input.read():
            matched_lines = self.grep_file(input.read().split('\n'))
            if matched_lines:
                result.append(matched_lines)
            output.write('\n'.join(result))
        return 0


class Wc(Command):
    """ Class for bash command wc - print newline, word, and byte counts for each file. """

    def str_statistics(self, text):
        lines = len(text.split('\n'))
        words = len(text.split())
        bytes = len(text.encode('utf-8'))
        return '{}  {}  {}'.format(lines, words, bytes)

    def file_statistics(self, file):
        with open(file, 'r') as f:
            content = f.read()
            counts = self.str_statistics(content)
        return '{}  {}'.format(counts, file)

    def execute(self, env, input, output):
        result = []
        if self.args:
            try:
                for arg in self.args:
                    result.append(self.file_statistics(arg))
            except IOError as e:
                raise CommandException('wc', e)
            output.write("\n".join(result))
        elif input.read():
            output.write(self.str_statistics(input.read()))
        return 0


class External(Command):
    """ Class for bash external command - execute command in new subprocess. """

    def __init__(self, name, args):
        super().__init__(args)
        self.name = name

    def execute(self, env, input, output):
        if not self.args:
            self.args = []
        try:
            process = subprocess.Popen([self.name] + self.args, universal_newlines=True,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate(input.read())
            if len(err) != 0:
                raise CommandException('external', err)
            output.write(out.strip())
        except (subprocess.SubprocessError, FileExistsError, FileNotFoundError) as e:
            raise CommandException('external', e)
        return process.returncode
