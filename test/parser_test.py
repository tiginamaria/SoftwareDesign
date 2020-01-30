import unittest

from src.interpreter.commands import Echo, Cat, Pwd, Exit, Wc, External
from src.parser.parser import Parser


class TestStringMethods(unittest.TestCase):

    def test_parse_echo_command(self):
        parser = Parser()
        pipe = parser.parse("echo 'text.pdf' 123 \"hw.tex\"")
        self.assertTrue(len(pipe) == 1)
        echo = pipe[0]
        self.assertIsInstance(echo, Echo)
        self.assertEqual({'text.pdf', '123', 'hw.tex'}, set(echo.args))

    def test_parse_cat_command(self):
        parser = Parser()
        pipe = parser.parse("cat 'text.txt' \"hw.tex\" file")
        self.assertTrue(len(pipe) == 1)
        cat = pipe[0]
        self.assertIsInstance(cat, Cat)
        self.assertEqual({'text.txt', 'hw.tex', 'file'}, set(cat.args))

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
        self.assertEqual({'text.txt', 'image.jpg', 'file'}, set(wc.args))

    def test_parse_pipe_all_tokens(self):
        parser = Parser()
        pipe = parser.parse("cat \"file1\" 'file2' | echo ab\"cd\" 'ef' | git commit -m \"hello\" | pwd | wc")
        self.assertTrue(len(pipe) == 5)

        cat = pipe[0]
        self.assertEqual({'file1', 'file2'}, set(cat.args))
        self.assertIsInstance(cat, Cat)

        echo = pipe[1]
        self.assertIsInstance(echo, Echo)
        self.assertEqual({'abcd', 'ef'}, set(echo.args))

        external = pipe[2]
        self.assertIsInstance(external, External)
        self.assertEqual({'commit', '-m', '\"hello\"'}, set(external.args))

        pwd = pipe[3]
        self.assertIsInstance(pwd, Pwd)
        self.assertIsNone(pwd.args)

        wc = pipe[4]
        self.assertIsInstance(wc, Wc)
        self.assertIsNone(wc.args)


if __name__ == '__main__':
    unittest.main()
