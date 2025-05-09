import unittest
from lab3.views.expression_nodes import clean_input, parse_symbols


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

    # Новые тесты для валидации
    def test_clean_input_non_string(self):
        with self.assertRaises(ValueError):
            clean_input(123)
        with self.assertRaises(ValueError):
            clean_input(None)
        with self.assertRaises(ValueError):
            clean_input(["A & B"])

    def test_parse_symbols_non_string(self):
        with self.assertRaises(ValueError):
            parse_symbols(123)
        with self.assertRaises(ValueError):
            parse_symbols(None)
        with self.assertRaises(ValueError):
            parse_symbols(["A->B"])

    def test_parse_symbols_empty_string(self):
        with self.assertRaises(ValueError):
            parse_symbols("")
        with self.assertRaises(ValueError):
            parse_symbols("   ")

    def test_parse_symbols_invalid_chars(self):
        with self.assertRaises(ValueError) as context:
            parse_symbols("A@B")
        self.assertIn("Invalid symbol at position 1", str(context.exception))

        with self.assertRaises(ValueError) as context:
            parse_symbols("A#B")
        self.assertIn("Invalid symbol at position 1", str(context.exception))

    def test_parse_symbols_partial_implication(self):
        with self.assertRaises(ValueError) as context:
            parse_symbols("A-")
        self.assertIn("Invalid symbol at position 1", str(context.exception))

    def test_parse_symbols_complex_invalid(self):
        with self.assertRaises(ValueError):
            parse_symbols("A & B + C")
        with self.assertRaises(ValueError):
            parse_symbols("A -> B ->")

    def test_parse_symbols_edge_cases(self):
        # Проверка на один символ
        self.assertEqual(parse_symbols("A"), ['A'])
        self.assertEqual(parse_symbols("!"), ['!'])

        # Проверка на несколько одинаковых операторов
        self.assertEqual(parse_symbols("!!A"), ['!', '!', 'A'])
        self.assertEqual(parse_symbols("A||B"), ['A', '|', '|', 'B'])

