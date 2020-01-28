from src.parser.commands.cat import Cat
from src.parser.commands.echo import Echo
from src.parser.commands.exit import Exit
from src.parser.commands.external import External
from src.parser.commands.pwd import Pwd
from src.parser.commands.wc import Wc


class CommandFactory:
    standard_commands = ['cat', 'echo', 'exit', 'pwd', 'wc']

    def create(self, name, args):
        if name in self.standard_commands:
            if name == 'cat':
                return Cat(args)
            elif name == 'echo':
                return Echo(args)
            elif name == 'exit':
                return Exit(args)
            elif name == 'pwd':
                return Pwd(args)
            elif name == 'wc':
                return Wc(args)
        else:
            return External(args, name)
