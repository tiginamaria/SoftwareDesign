import unittest

from src.environment import Environment
from src.substituter.substituter import Substituter, SubstituterException


class TestStringMethods(unittest.TestCase):

    def test_substitution_double_quotes(self):
        env = Environment({'cat': '1'})
        substituter = Substituter(env)
        text = substituter.substitute("\"echo dog   $cat  rat\"")
        self.assertEqual("\"echo dog   1  rat\"", text)

    def test_substitution_no_quotes(self):
        env = Environment({'cat': '1', 'dog': '2'})
        substituter = Substituter(env)
        text = substituter.substitute("echo $dog   $cat  rat")
        self.assertEqual("echo 2   1  rat", text)

    def test_substitution_separated_different_quotes(self):
        env = Environment({'cat': '1', 'dog': '2', 'rat': '3'})
        substituter = Substituter(env)
        text = substituter.substitute("echo '$cat'   \"$dog\"  $rat")
        self.assertEqual("echo '$cat'   \"2\"  3", text)

    def test_substitution_different_quotes(self):
        env = Environment({'cat': '1', 'dog': '2', 'rat': '3'})
        substituter = Substituter(env)
        text = substituter.substitute("echo '$cat'\"$dog\"$rat")
        self.assertEqual("echo '$cat'\"2\"3", text)
        text = substituter.substitute("echo $cat$dog$rat")
        self.assertEqual("echo 123", text)

    def test_substitution_empty_variable(self):
        env = Environment(dict())
        substituter = Substituter(env)
        self.assertRaises(SubstituterException, substituter.substitute, "echo $")
        self.assertRaises(SubstituterException, substituter.substitute, "echo \"$\"")
        try:
            substituter.substitute("echo '$'")
        except SubstituterException:
            self.fail("should not raise exception")

    def test_substitution_empty_quotes(self):
        env = Environment(dict())
        substituter = Substituter(env)
        text = substituter.substitute("echo ''\"\"  ")
        self.assertEqual("echo ''\"\"  ", text)


if __name__ == '__main__':
    unittest.main()
