import unittest

# Импортируем необходимые функции и классы
from lab3.views.expression_nodes import ExpressionNode, clean_input, parse_symbols
from lab3.views.formula_tree_generator import dijkstra_algorithm, convert_to_tree, build_formula_tree  # замените 'your_module' на имя файла, где находятся ваши функции

class TestExpressionParser(unittest.TestCase):

    def test_clean_input(self):
        self.assertEqual(clean_input("a & b "), "a&b")
        self.assertEqual(clean_input(" ! a "), "!a")
        self.assertEqual(clean_input(" ( a | b ) "), "(a|b)")

    def test_parse_symbols(self):
        self.assertEqual(parse_symbols("a & b"), ['a', '&', 'b'])
        self.assertEqual(parse_symbols("a -> b"), ['a', '->', 'b'])
        self.assertEqual(parse_symbols("!(a & b)"), ['!', '(', 'a', '&', 'b', ')'])

    def test_dijkstra_algorithm(self):
        self.assertEqual(dijkstra_algorithm(['a', '&', 'b']), ['a', 'b', '&'])
        self.assertEqual(dijkstra_algorithm(['a', '->', 'b']), ['a', 'b', '->'])
        self.assertEqual(dijkstra_algorithm(['!', 'a']), ['a', '!'])
        self.assertEqual(dijkstra_algorithm(['a', '&', 'b', '|', 'c']), ['a', 'b', '&', 'c', '|'])


    def test_build_formula_tree(self):
        input_str = "a & b"
        tree = build_formula_tree(input_str)
        self.assertEqual(tree.operation, 'conjunction')
        self.assertEqual(tree.lhs.variable, 'a')
        self.assertEqual(tree.rhs.variable, 'b')

        input_str = "!(a | b)"
        tree = build_formula_tree(input_str)
        self.assertEqual(tree.operation, 'negation')
        self.assertEqual(tree.lhs.operation, 'disjunction')
        self.assertEqual(tree.lhs.lhs.variable, 'a')
        self.assertEqual(tree.lhs.rhs.variable, 'b')

if __name__ == '__main__':
    unittest.main()