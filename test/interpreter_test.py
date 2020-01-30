import unittest

from src.environment import Environment
from src.interpreter.commands import Cat, Echo
from src.interpreter.interpreter import Interpreter


class TestStringMethods(unittest.TestCase):

    def test_cat(self):
        env = Environment({'cat': '1'})
        interpreter = Interpreter(env)
        with open('resources/file.txt', 'r') as f:
            print(f.read())
        interpreter.interpret([Cat(['resources/file.txt'])])

    def test_echo(self):
        env = Environment({'cat': '1'})
        interpreter = Interpreter(env)
        interpreter.interpret([Echo(['\"hello\"'])])

    def test_pwd(self):
        pass

    def test_wc(self):
        pass

    def test_evaluation(self):
        pass

    def test_assignment(self):
        pass


if __name__ == '__main__':
    unittest.main()
