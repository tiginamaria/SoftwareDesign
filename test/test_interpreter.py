import os
import subprocess
import unittest
from pathlib import Path

from src.environment import Environment
from src.interpreter.commands import Cat, Echo, Wc, External, Pwd, Assignment, Cd, Ls
from src.interpreter.interpreter import Interpreter, InterpreterException


class InterpreterTests(unittest.TestCase):
    def setUp(self):
        self.file1 = "test/resources/text1"
        self.file2 = "test/resources/text2"
        self.non_existent_file = "test/resources/text3"

    def test_cat_one_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cat([self.file1])])
        self.assertEqual(0, code)
        self.assertEqual("Cat   dog\n    rat\n", output)

    def test_cat_many_args(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cat([self.file1, self.file2])])
        self.assertEqual(0, code)
        self.assertEqual("Cat   dog\n    rat\nhello Hi\n\nbye ByE", output)

    def test_cat_on_same_file(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cat([self.file1, self.file1])])
        self.assertEqual(0, code)
        self.assertEqual("Cat   dog\n    rat\nCat   dog\n    rat\n", output)

    def test_cat_exception(self):
        interpreter = Interpreter(Environment(dict()))
        self.assertRaises(InterpreterException, interpreter.interpret, [Cat([self.file1, self.non_existent_file])])

    def test_cat_no_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cat(None)])
        self.assertEqual(0, code)
        self.assertIsNone(output)

    def test_cat_no_args_input(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['cat', 'dog']), Cat(None)])
        self.assertEqual(0, code)
        self.assertEqual("cat dog", output)

    def test_cat_one_arg_input(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['cat', 'dog']), Cat([self.file1])])
        self.assertEqual(0, code)
        self.assertEqual("Cat   dog\n    rat\n", output)

    def test_echo_one_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['cat'])])
        self.assertEqual(0, code)
        self.assertEqual("cat", output)

    def test_echo_many_args(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['cat', 'D.o,g', ' R     at '])])
        self.assertEqual(0, code)
        self.assertEqual("cat D.o,g  R     at ", output)

    def test_echo_no_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(None)])
        self.assertEqual(0, code)
        self.assertEqual("", output)

    def test_cat_echo(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cat([self.file1]), Echo(['cat', 'dog'])])
        self.assertEqual(0, code)
        self.assertEqual("cat dog", output)

    def test_wc_one_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Wc([self.file1])])
        self.assertEqual(0, code)
        self.assertEqual('3  3  18  {}'.format(self.file1), output)

    def test_wc_many_args(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Wc([self.file1, self.file2])])
        self.assertEqual(0, code)
        self.assertEqual('3  3  18  {}\n3  4  17  {}'.format(self.file1, self.file2), output)

    def test_wc_on_same_file(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Wc([self.file1, self.file1])])
        self.assertEqual(0, code)
        self.assertEqual('3  3  18  {}\n3  3  18  {}'.format(self.file1, self.file1), output)

    def test_wc_exception(self):
        interpreter = Interpreter(Environment(dict()))
        self.assertRaises(InterpreterException, interpreter.interpret, [Wc([self.file1, self.non_existent_file])])

    def test_wc_no_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Wc(None)])
        self.assertEqual(0, code)
        self.assertIsNone(output)

    def test_external(self):
        interpreter = Interpreter(Environment(dict()))
        expected_output = subprocess.getoutput("git status").strip()
        code, output = interpreter.interpret([External('git', ['status'])])
        self.assertEqual(0, code)
        self.assertEqual(expected_output, output)

        expected_output = subprocess.getoutput("git --version").strip()
        code, output = interpreter.interpret([External('git', ['--version'])])
        self.assertEqual(0, code)
        self.assertEqual(expected_output, output)

    def test_external_exception(self):
        interpreter = Interpreter(Environment(dict()))
        self.assertRaises(InterpreterException, interpreter.interpret, [External('git', ['--lol'])])

    def test_pwd_no_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Pwd(None)])
        self.assertEqual(os.getcwd(), output)

    def test_pwd_many_args(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Pwd(['cat', 'dog', 'rat'])])
        self.assertEqual(os.getcwd(), output)

    def test_assignment(self):
        env = Environment(dict())
        interpreter = Interpreter(env)
        code, output = interpreter.interpret([Assignment(['x', '1'])])
        self.assertEqual(0, code)
        self.assertEqual('1', env['x'])
        code, output = interpreter.interpret([Assignment(['x', '2'])])
        self.assertEqual(0, code)
        self.assertEqual('2', env['x'])

    def test_echo_wc_commands(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['123456']), Wc(None)])
        self.assertEqual(0, code)
        self.assertEqual('1  1  6', output)

    def test_cat_wc_commands(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cat([self.file1]), Wc(None)])
        self.assertEqual(0, code)
        self.assertEqual('3  3  18', output)

    def test_echo_cat_commands(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['cat', 'dog']), Wc(None), Cat(None)])
        self.assertEqual(0, code)
        self.assertEqual('1  2  7', output)

    def test_cd_without_args(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cd(), Pwd()])
        self.assertEqual(0, code)
        self.assertEqual(str(Path.home()), output)

    def test_cd_with_existing_arg(self):
        interpreter = Interpreter(Environment(dict()))
        old_directory = os.getcwd()
        code, output = interpreter.interpret([Cd(['test/resources']), Pwd()])
        self.assertEqual(0, code)
        self.assertEqual(old_directory + '/test/resources', output)

    def test_cd_ignores_pipe(self):
        interpreter = Interpreter(Environment(dict()))
        old_directory = os.getcwd()
        code, output = interpreter.interpret([Echo(['test/resources']), Cd(), Pwd()])
        self.assertEqual(0, code)
        self.assertEqual(old_directory, output)

    def test_cd_to_parent(self):
        interpreter = Interpreter(Environment(dict()))
        old_directory = os.getcwd()
        code, output = interpreter.interpret([Cd(['test/resources']), Cd(['..']), Pwd()])
        self.assertEqual(0, code)
        self.assertEqual(old_directory, output)

    def test_cd_with_many_args(self):
        interpreter = Interpreter(Environment(dict()))
        self.assertRaises(InterpreterException, interpreter.interpret, [Cd(['test/resources', '..'])])

    def test_cd_with_absolute_path(self):
        interpreter = Interpreter(Environment(dict()))
        old_directory = os.getcwd()
        code, output = interpreter.interpret([Cd([old_directory + '/test/resources']), Pwd()])
        self.assertEqual(0, code)
        self.assertEqual(old_directory + '/test/resources', output)

    def test_ls_no_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cd(['test/resources']), Ls()])
        self.assertEqual(0, code)
        self.assertEqual('\n'.join(['text1', 'text2']), output)

    def test_ls_one_arg(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Ls(['test/resources'])])
        self.assertEqual(0, code)
        self.assertEqual('\n'.join(['text1', 'text2']), output)

    def test_ls_from_pipe(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Echo(['test/resources']), Ls()])
        self.assertEqual(0, code)
        self.assertEqual('\n'.join(['text1', 'text2']), output)

    def test_ls_several_args(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Ls(['test/resources', 'test/resources'])])
        self.assertEqual(0, code)
        self.assertEqual('\n'.join(['text1', 'text2', 'text1', 'text2']), output)

    def test_ls_ignores_several_args_from_pipe(self):
        interpreter = Interpreter(Environment(dict()))
        code, output = interpreter.interpret([Cd(['test/resources']),
                                              Echo(['test', 'test']),
                                              Ls()])
        self.assertEqual(0, code)
        self.assertEqual('\n'.join(['text1', 'text2']), output)


if __name__ == '__main__':
    unittest.main()
