import unittest

from src.interpreter.commands import Echo, Cat, Pwd, Exit, Wc, External, Grep
from src.parser.parser import Parser


class TestStringMethods(unittest.TestCase):

    def test_parse_echo_command(self):
        parser = Parser()
        pipe = parser.parse("echo 'text1.pdf' 123 \"hw.tex\"   !.-+=")
        self.assertTrue(len(pipe) == 1)
        echo = pipe[0]
        self.assertIsInstance(echo, Echo)
        self.assertEqual({'text1.pdf', '123', 'hw.tex', '!.-+='}, set(echo.args))

    def test_parse_cat_command(self):
        parser = Parser()
        pipe = parser.parse("cat 'text1' \"hw.tex\" file")
        self.assertTrue(len(pipe) == 1)
        cat = pipe[0]
        self.assertIsInstance(cat, Cat)
        self.assertEqual({'text1', 'hw.tex', 'file'}, set(cat.args))

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
        pipe = parser.parse("wc file 'text1' \"image.jpg\"")
        self.assertTrue(len(pipe) == 1)
        wc = pipe[0]
        self.assertIsInstance(wc, Wc)
        self.assertEqual({'text1', 'image.jpg', 'file'}, set(wc.args))

    def test_parse_grep_command(self):
        parser = Parser()
        pipe = parser.parse("grep -A 6 -i file 'text1' \"image.jpg\"")
        self.assertTrue(len(pipe) == 1)
        grep = pipe[0]
        self.assertIsInstance(grep, Grep)
        self.assertEqual(6, grep.args.A)
        self.assertFalse(grep.args.w)
        self.assertTrue(grep.args.i)
        self.assertEqual({'image.jpg', 'text1'}, set(grep.args.files))
        self.assertEqual('file', grep.args.pattern)

    def test_blanks_tokens(self):
        parser = Parser()
        pipe = parser.parse("cat   \"file1   \"     'file2'|echo ab\"  c  d\"    '     ef'  |   wc    ")
        cat = pipe[0]
        self.assertEqual({'file1   ', 'file2'}, set(cat.args))
        self.assertIsInstance(cat, Cat)

        echo = pipe[1]
        self.assertIsInstance(echo, Echo)
        self.assertEqual({'ab  c  d', '     ef'}, set(echo.args))

        wc = pipe[2]
        self.assertIsInstance(wc, Wc)
        self.assertIsNone(wc.args)

    def test_parse_pipe_all_tokens(self):
        parser = Parser()
        pipe = parser.parse("cat \"file1\" 'file2' | echo ab\"cd\" 'ef' | git commit -m \"hello\" | pwd | wc | grep 1")
        self.assertTrue(len(pipe) == 6)

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

        grep = pipe[5]
        self.assertIsInstance(grep, Grep)
        self.assertEqual(1, grep.args.A)
        self.assertFalse(grep.args.w)
        self.assertFalse(grep.args.i)
        self.assertEqual(0, len(grep.args.files))
        self.assertEqual('1', grep.args.pattern)


if __name__ == '__main__':
    unittest.main()
