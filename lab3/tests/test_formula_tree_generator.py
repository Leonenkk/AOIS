import unittest
from lab3.views.expression_nodes import ExpressionNode, clean_input, parse_symbols
from lab3.views.formula_tree_generator import dijkstra_algorithm, convert_to_tree, build_formula_tree

class TestExpressionParser(unittest.TestCase):
    def test_clean_input(self):
        self.assertEqual(clean_input("a & b "), "a&b")
        self.assertEqual(clean_input(" ! a "), "!a")
        self.assertEqual(clean_input(" ( a | b ) "), "(a|b)")


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

    # Новые тесты для валидации dijkstra_algorithm
    def test_dijkstra_invalid_input(self):
        with self.assertRaises(TypeError):
            dijkstra_algorithm("not a list")
        with self.assertRaises(TypeError):
            dijkstra_algorithm([123, '&', 'b'])
        with self.assertRaises(ValueError):
            dijkstra_algorithm(['A', '&', 'b'])  # uppercase variable
        with self.assertRaises(ValueError):
            dijkstra_algorithm(['a', '-', 'b'])  # invalid implication
        with self.assertRaises(ValueError):
            dijkstra_algorithm(['a', '@', 'b'])  # unknown token
        with self.assertRaises(ValueError):
            dijkstra_algorithm(['a', ')'])  # mismatched parentheses
        with self.assertRaises(ValueError):
            dijkstra_algorithm(['('])  # unclosed parenthesis

    # Новые тесты для валидации convert_to_tree
    def test_convert_to_tree_invalid_input(self):
        with self.assertRaises(TypeError):
            convert_to_tree("not a list")
        with self.assertRaises(TypeError):
            convert_to_tree([123, '&', 'b'])
        with self.assertRaises(ValueError):
            convert_to_tree(['A', '&', 'b'])  # uppercase variable
        with self.assertRaises(ValueError):
            convert_to_tree(['!'])  # not enough operands
        with self.assertRaises(ValueError):
            convert_to_tree(['a', '&'])  # not enough operands
        with self.assertRaises(ValueError):
            convert_to_tree(['a', 'b'])  # too many operands
        with self.assertRaises(ValueError):
            convert_to_tree(['a', '@', 'b'])  # unknown element

    # Новые тесты для валидации build_formula_tree
    def test_build_formula_tree_invalid_input(self):
        with self.assertRaises(TypeError):
            build_formula_tree(123)
        with self.assertRaises(ValueError):
            build_formula_tree("")
        with self.assertRaises(ValueError):
            build_formula_tree("   ")
        with self.assertRaises(ValueError):
            build_formula_tree("A & b")  # uppercase variable
        with self.assertRaises(ValueError):
            build_formula_tree("a @ b")  # invalid symbol
        with self.assertRaises(ValueError):
            build_formula_tree("(a & b")  # mismatched parentheses


    def test_convert_to_tree_empty_input(self):
        with self.assertRaises(ValueError):
            convert_to_tree([])

    def test_complex_expressions(self):
        # Тестирование сложных выражений
        expr = "!(a & b) -> (c | d)"
        tree = build_formula_tree(expr)
        self.assertEqual(tree.operation, 'implication')
        self.assertEqual(tree.lhs.operation, 'negation')
        self.assertEqual(tree.rhs.operation, 'disjunction')

        expr = "a ~ b ~ c"
        tree = build_formula_tree(expr)
        self.assertEqual(tree.operation, 'equivalence')
        self.assertEqual(tree.rhs.variable, 'c')

