import os
import subprocess
import unittest

from src.cli import CLI
from src.interpreter.interpreter import InterpreterException
from src.parser.parser import ParserException
from src.substituter.substituter import SubstituterException


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.origin_dir = os.getcwd()

    def setUp(self):
        self.file1 = "test/resources/text1"
        self.file2 = "test/resources/text2"
        self.non_existent_file = "test/resources/text3"
        os.chdir(self.origin_dir)

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

    def test_cd(self):
        cli = CLI()
        self.assertEqual(None, cli.run("cd")[1])

    def test_ls(self):
        cli = CLI()
        output = cli.run(f'ls {os.getcwd() + "/test/resources"}')[1]
        self.assertSetEqual({'text1', 'text2'}, set(output.split('\n')))

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


if __name__ == '__main__':
    unittest.main()
