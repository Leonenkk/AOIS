import unittest

from lab3.views.expression_nodes import clean_input, parse_symbols  # Замените на имя вашего модуля

class TestExpressionParser(unittest.TestCase):

    def test_clean_input_removes_spaces(self):
        self.assertEqual(clean_input("A & B"), "A&B")
        self.assertEqual(clean_input(" ( A -> B ) "), "(A->B)")
        self.assertEqual(clean_input("! A | B "), "!A|B")

    def test_parse_symbols_basic(self):
        self.assertEqual(parse_symbols("A&B"), ['A', '&', 'B'])
        self.assertEqual(parse_symbols("A|B"), ['A', '|', 'B'])
        self.assertEqual(parse_symbols("!A"), ['!', 'A'])

    def test_parse_symbols_with_parentheses(self):
        self.assertEqual(parse_symbols("(A&B)"), ['(', 'A', '&', 'B', ')'])
        self.assertEqual(parse_symbols("((A))"), ['(', '(', 'A', ')', ')'])

    def test_parse_symbols_with_implication(self):
        self.assertEqual(parse_symbols("A->B"), ['A', '->', 'B'])
        self.assertEqual(parse_symbols("(A->B)"), ['(', 'A', '->', 'B', ')'])

    def test_parse_symbols_mixed(self):
        self.assertEqual(parse_symbols("!(A->B)&C"), ['!', '(', 'A', '->', 'B', ')', '&', 'C'])
        self.assertEqual(parse_symbols("A->(B|C)"), ['A', '->', '(', 'B', '|', 'C', ')'])

if __name__ == '__main__':
    unittest.main()