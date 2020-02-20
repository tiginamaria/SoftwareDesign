import unittest

from src.interpreter.commands import Echo, Cat, Pwd, Exit, Wc, External, Ls, Cd
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

    def test_parse_cd_command(self):
        parser = Parser()
        pipe = parser.parse("cd \"dir\"")
        self.assertTrue(len(pipe) == 1)
        cd = pipe[0]
        self.assertIsInstance(cd, Cd)
        self.assertEqual({'dir'}, set(cd.args))

    def test_parse_ls_command(self):
        parser = Parser()
        pipe = parser.parse("ls \"dir\"")
        self.assertTrue(len(pipe) == 1)
        ls = pipe[0]
        self.assertIsInstance(ls, Ls)
        self.assertEqual({'dir'}, set(ls.args))

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
        pipe = parser.parse(
            "cat \"file1\" 'file2' | echo ab\"cd\" 'ef' | git commit -m \"hello\" | pwd | wc | ls | cd"
        )
        self.assertTrue(len(pipe) == 7)

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

        ls = pipe[5]
        self.assertIsInstance(ls, Ls)
        self.assertIsNone(ls.args)

        cd = pipe[6]
        self.assertIsInstance(cd, Cd)
        self.assertIsNone(cd.args)


if __name__ == '__main__':
    unittest.main()
