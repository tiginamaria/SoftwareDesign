import unittest

from src.parser.commands.cat import Cat
from src.parser.commands.echo import Echo
from src.parser.commands.exit import Exit
from src.parser.commands.wc import Wc
from src.parser.commands.pwd import Pwd
from src.parser.parser import Parser


class TestStringMethods(unittest.TestCase):

    def test_parse_echo_command(self):
        parser = Parser()
        pipe = parser.parse("echo 'text.pdf' 123 \"hw.tex\"")
        self.assertTrue(len(pipe) == 1)
        echo = pipe[0]
        self.assertIsInstance(echo, Echo)
        self.assertEqual({'\'text.pdf\'', '123', '\"hw.tex\"'}, set(echo.args))

    def test_parse_cat_command(self):
        parser = Parser()
        pipe = parser.parse("cat 'text.txt' \"hw.tex\" file")
        self.assertTrue(len(pipe) == 1)
        cat = pipe[0]
        self.assertIsInstance(cat, Cat)
        self.assertEqual({'\'text.txt\'', '\"hw.tex\"', 'file'}, set(cat.args))

    def test_parse_pwd_command(self):
        parser = Parser()
        pipe = parser.parse("pwd")
        self.assertTrue(len(pipe) == 1)
        pwd = pipe[0]
        self.assertIsInstance(pwd, Pwd)
        self.assertIsNone(pwd.args)

    def test_parse_exit_command(self):
        parser = Parser()
        pipe = parser.parse("exit")
        self.assertTrue(len(pipe) == 1)
        exit = pipe[0]
        self.assertIsInstance(exit, Exit)
        self.assertIsNone(exit.args)

    def test_parse_wc_command(self):
        parser = Parser()
        pipe = parser.parse("wc file 'text.txt' \"image.jpg\"")
        self.assertTrue(len(pipe) == 1)
        wc = pipe[0]
        self.assertIsInstance(wc, Wc)
        self.assertEqual({'\'text.txt\'', '\"image.jpg\"', 'file'}, set(wc.args))

    def test_parse_pipe(self):
        parser = Parser()
        pipe = parser.parse("cat \"file\" | echo 123 | wc")
        self.assertTrue(len(pipe) == 3)
        cat = pipe[0]
        self.assertEqual({'\"file\"'}, set(cat.args))
        self.assertIsInstance(cat, Cat)
        echo = pipe[1]
        self.assertIsInstance(echo, Echo)
        self.assertEqual({'123'}, set(echo.args))
        wc = pipe[2]
        self.assertIsInstance(wc, Wc)
        self.assertIsNone(wc.args)


if __name__ == '__main__':
    unittest.main()
