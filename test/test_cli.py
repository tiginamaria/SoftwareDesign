import os
import subprocess
import unittest

from src.cli import CLI
from src.interpreter.interpreter import InterpreterException
from src.parser.command_factory import ArgumentParserException
from src.parser.parser import ParserException
from src.substituter.substituter import SubstituterException


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.file1 = "test/resources/text1"
        self.file2 = "test/resources/text2"
        self.non_existent_file = "test/resources/text3"
        self.file_grep_A = "test/resources/text_grep_A"
        self.file_grep_w = "test/resources/text_grep_w_i"
        self.file_grep_i = "test/resources/text_grep_w_i"
        self.file_grep_all = "test/resources/text_grep_A_w_i"

    def test_cat(self):
        cli = CLI()
        self.assertEqual('', cli.run("echo | cat")[1])
        self.assertEqual('cat dog rat', cli.run("echo \"cat\" 'dog' rat | cat")[1])
        self.assertEqual("Cat   dog\n    rat\n", cli.run("cat {}".format(self.file1))[1])
        self.assertEqual('Cat   dog\n    rat\nhello Hi\n\nbye ByE', cli.run("cat {} {}"
                                                                            .format(self.file1, self.file2))[1])

    def test_cat_exception(self):
        cli = CLI()
        self.assertRaises(InterpreterException, cli.run, "cat {}".format(self.non_existent_file))
        self.assertRaises(InterpreterException, cli.run, "{} {}".format(self.file1, self.non_existent_file))

    def test_echo(self):
        cli = CLI()
        self.assertEqual('', cli.run("    echo    ")[1])
        self.assertEqual('', cli.run("echo \"\"")[1])
        self.assertEqual('', cli.run("echo ''")[1])
        self.assertEqual('123123123', cli.run("echo 123'123'\"123\"")[1])
        self.assertEqual('cat dog rat 123!@ *', cli.run("echo \"cat\"   'dog'  rat '123'!@ * ")[1])

    def test_pwd(self):
        cli = CLI()
        self.assertEqual(os.getcwd(), cli.run("pwd")[1])

    def test_wc(self):
        cli = CLI()
        self.assertEqual("3  3  18  {}".format(self.file1), cli.run("wc {}".format(self.file1))[1])
        self.assertEqual('3  3  18', cli.run("cat {} | wc".format(self.file1))[1])
        self.assertEqual("3  3  18  {}\n3  4  17  {}".format(self.file1, self.file2),
                         cli.run("wc {} {}".format(self.file1, self.file2))[1])

    def test_wc_exception(self):
        cli = CLI()
        self.assertRaises(InterpreterException, cli.run, "wc {}".format(self.non_existent_file))

    def test_assignment(self):
        cli = CLI()
        self.assertEqual(0, cli.run("x=123")[0])
        self.assertEqual('123', cli.run("echo $x")[1])
        self.assertEqual(0, cli.run("x=$x")[0])
        self.assertEqual('123', cli.run("echo $x")[1])
        self.assertEqual(0, cli.run("abcABC=$x")[0])
        self.assertEqual('123', cli.run("echo $abcABC")[1])
        self.assertEqual(0, cli.run("x=123abc!")[0])
        self.assertEqual('123abc!', cli.run("echo $x")[1])
        self.assertEqual(0, cli.run("x=123'123'\"123\"")[0])
        self.assertEqual('123123123', cli.run("echo $x")[1])

    def test_assignment_exception(self):
        cli = CLI()
        self.assertRaises(ParserException, cli.run, "x=123 123")

    def test_evaluation(self):
        cli = CLI()
        self.assertEqual(0, cli.run("x=123")[0])
        self.assertEqual(0, cli.run("abc=abc")[0])
        self.assertEqual(0, cli.run("A1=!")[0])
        self.assertEqual(0, cli.run("file={}".format(self.file1))[0])
        self.assertEqual('123 $x 123', cli.run("echo $x '$x' \"$x\"")[1])
        self.assertEqual('Cat   dog\n    rat\n', cli.run("echo $x '$x' \"$x\" | cat $file")[1])
        self.assertEqual('123$x123', cli.run("echo $x'$x'\"$x\"")[1])
        self.assertEqual('123 $abc !', cli.run("echo $x '$abc' \"$A1\"")[1])
        self.assertEqual('', cli.run("echo \"\"")[1])
        self.assertEqual('', cli.run("echo ''")[1])

        self.assertEqual(0, cli.run("x=ec")[0])
        self.assertEqual(0, cli.run("y=ho")[0])
        self.assertEqual(0, cli.run("z=magic")[0])
        self.assertEqual('magic', cli.run("$x$y $z")[1])

    def test_evaluation_exception(self):
        cli = CLI()
        self.assertEqual(0, cli.run("x=no_file")[0])
        self.assertRaises(InterpreterException, cli.run, "echo $x | cat '$x'")
        self.assertRaises(SubstituterException, cli.run, "echo $")

    def test_external(self):
        cli = CLI()
        expected_output = subprocess.getoutput("git status").strip()
        code, output = cli.run("git status")
        self.assertEqual(0, code)
        self.assertEqual(expected_output, output)

    def test_external_exception(self):
        cli = CLI()
        self.assertRaises(InterpreterException, cli.run, "git lol")

    def test_grep(self):
        cli = CLI()
        self.assertIsNone(cli.run("echo | grep abc")[1])
        self.assertEqual('1  1  3', cli.run("echo abc | grep abc | wc")[1])
        self.assertEqual('abc', cli.run("echo abc | grep '^a.*$'")[1])
        self.assertEqual('cat\ndog\ncat cat\ncatdog\nRat', cli.run("grep -A 3 cat {}".format(self.file_grep_A))[1])
        self.assertEqual('dog\ncat cat\ndog rat\nrat\ndog\ncatdog\n', cli.run("grep -A 2 dog {}"
                                                                              .format(self.file_grep_A))[1])
        self.assertEqual('dog rat\nrat\n', cli.run("grep rat {}".format(self.file_grep_A))[1])
        self.assertEqual('cat, dog!\n', cli.run("grep -w cat {}".format(self.file_grep_w))[1])
        self.assertEqual('cat, dog!\ncaTCaT\nHELLO, CAT.', cli.run("grep -i cat {}".format(self.file_grep_i))[1])
        self.assertEqual('cat, dog!\ndoGgg\ncAT. dog\nno...dogs\nHELLO, CAT.', cli.run("grep -A 2 -i -w cat {}"
                                                                                       .format(self.file_grep_all))[1])

    def test_grep_exception(self):
        cli = CLI()
        self.assertRaises(ArgumentParserException, cli.run, "grep")


if __name__ == '__main__':
    unittest.main()
