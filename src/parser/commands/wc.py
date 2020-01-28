from src.parser.commands.command import Command


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

    def execute(self, env, stream):
        if self.args:
            for arg in self.args:
                print(arg)
                try:
                    stream.append(self.file_statistics(arg))
                except IOError as exception:
                    print('wc : {}'.format(exception))
        else:
            stream.write(self.str_statistics(stream.read()[0]))
