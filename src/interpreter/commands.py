import os
import subprocess
from pathlib import Path

from src.environment import Environment
from src.io.stream_io import StreamIO


class ExecutableCommandException(Exception):
    """ Exception raises in case of wrong command behaviour. """

    def __init__(self, name, message):
        super(ExecutableCommandException, self).__init__("{}: {}".format(name, message))


class ExecutableCommand:
    """ Base abstract class to emulate bash commands."""

    def __init__(self, args=None):
        """ Initialise arguments. """
        if args:
            self.args = args
        else:
            self.args = []

    def execute(self, env: Environment, input: StreamIO, output: StreamIO) -> int:
        """ Execute command.
        :param env: environment
        :param input: stream to read input from
        :param output: stream to write output to
        :return: code: return code (0) - successful execution to continue, (-1) - program should be interrupted
        :raise: CommandException: in case of improper execution
        """
        pass


class Assignment(ExecutableCommand):
    """ Class emulate bash assignment - add new variable to environment."""

    def execute(self, env, input, output):
        variable, value = self.args
        env[variable] = value
        return 0


class Cat(ExecutableCommand):
    """ Class emulate bash command cat - concatenate files and print on the standard output. """

    def execute(self, env, input, output):
        result = ""
        if self.args:
            try:
                for file in self.args:
                    with open(file, "r") as f:
                        result += f.read()
            except IOError as e:
                raise ExecutableCommandException('cat', e)
        else:
            result = input.read()
        output.write(result)
        return 0


class Echo(ExecutableCommand):
    """" Class emulate bash command echo - display a line of text. """

    def execute(self, env, input, output):
        if self.args:
            output.write(" ".join(self.args))
        else:
            output.write("")
        return 0


class Exit(ExecutableCommand):
    """ Class emulate bash command exit - cause normal process termination. """

    def execute(self, env, input, output):
        return -1


class Pwd(ExecutableCommand):
    """ Class for bash command pwd - print name of current/working directory. """

    def execute(self, env, input, output):
        output.write(os.getcwd())
        return 0


class Wc(ExecutableCommand):
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
                raise ExecutableCommandException('wc', e)
            output.write("\n".join(result))
        elif input.read():
            output.write(self.str_statistics(input.read()))
        return 0


class Cd(ExecutableCommand):
    """ Class for bash command cd - change the current/working directory. """

    def execute(self, env, input, output):
        if len(self.args) > 1:
            raise ExecutableCommandException('cd', 'too many arguments')

        if self.args:
            path = self.args[0]
        else:
            # change to the home directory by default
            path = str(Path.home())

        try:
            os.chdir(path)
        except OSError as e:
            raise ExecutableCommandException('cd', e)
        return 0


class Ls(ExecutableCommand):
    """
    Class for bash command ls - list all files and directories in the given directory (directories).
    Uses the current/working directory if no arguments are passes.
    """

    def execute(self, env, input, output):
        paths = self.get_paths(input)
        result = []
        try:
            for directory in paths:
                file_names = os.listdir(directory)
                if file_names:
                    result.extend(file_names)
            output.write('\n'.join(result))
        except OSError as e:
            raise ExecutableCommandException('ls', e)
        return 0

    def get_paths(self, input):
        paths = self.args
        if not self.args:
            from_input = input.read()
            if not from_input:
                from_input = ''
            input_args = from_input.split()
            if len(input_args) == 1:
                paths = [input_args[0]]
            else:
                # use the current directory by default
                paths = [os.getcwd()]
        return paths


class External(ExecutableCommand):
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
                raise ExecutableCommandException('external', err)
            output.write(out.strip())
        except (subprocess.SubprocessError, FileExistsError, FileNotFoundError) as e:
            raise ExecutableCommandException('external', e)
        return process.returncode
