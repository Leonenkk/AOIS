import unittest
from lab3.views.formula_analysis_tools import (
    mark_subtrees,
    calculate_depth,
    gather_subtrees,
    evaluate_ast,
)
from lab3.views.expression_nodes import ExpressionNode


class TestFormulaAnalysisTools(unittest.TestCase):
    def test_mark_subtrees_variable(self):
        node = ExpressionNode(operation='variable', variable='P')
        mark_subtrees(node)
        self.assertEqual(node.formula, 'P')

    def test_mark_subtrees_negation(self):
        var = ExpressionNode(operation='variable', variable='Q')
        neg = ExpressionNode(operation='negation', lhs=var)
        mark_subtrees(neg)
        self.assertEqual(neg.formula, '¬Q')

    def test_mark_subtrees_negation_complex(self):
        p = ExpressionNode(operation='variable', variable='P')
        r = ExpressionNode(operation='variable', variable='R')
        disj = ExpressionNode(operation='disjunction', lhs=p, rhs=r)
        neg = ExpressionNode(operation='negation', lhs=disj)
        mark_subtrees(neg)
        self.assertEqual(disj.formula, 'P∨R')
        self.assertEqual(neg.formula, '¬(P∨R)')

    def test_mark_subtrees_binary_ops(self):
        p = ExpressionNode(operation='variable', variable='P')
        q = ExpressionNode(operation='variable', variable='Q')
        r = ExpressionNode(operation='variable', variable='R')
        conj = ExpressionNode(operation='conjunction', lhs=p, rhs=q)
        imp = ExpressionNode(operation='implication', lhs=conj, rhs=r)
        mark_subtrees(imp)
        self.assertEqual(conj.formula, 'P∧Q')
        self.assertEqual(imp.formula, 'P∧Q→R')

    def test_calculate_depth(self):
        p = ExpressionNode(operation='variable', variable='P')
        self.assertEqual(calculate_depth(p), 1)
        neg = ExpressionNode(operation='negation', lhs=p)
        self.assertEqual(calculate_depth(neg), 2)
        q = ExpressionNode(operation='variable', variable='Q')
        conj1 = ExpressionNode(operation='conjunction', lhs=p, rhs=q)
        conj2 = ExpressionNode(operation='conjunction', lhs=conj1,
                               rhs=ExpressionNode(operation='variable', variable='R'))
        self.assertEqual(calculate_depth(conj2), 3)

    def test_gather_subtrees(self):
        p = ExpressionNode(operation='variable', variable='P')
        q = ExpressionNode(operation='variable', variable='Q')
        r = ExpressionNode(operation='variable', variable='R')
        conj = ExpressionNode(operation='conjunction', lhs=p, rhs=q)
        disj = ExpressionNode(operation='disjunction', lhs=conj, rhs=r)
        mark_subtrees(disj)
        subs = gather_subtrees(disj)
        formulas = {node.formula for node in subs}
        expected = {'P', 'Q', 'P∧Q', 'R', 'P∧Q∨R'}
        self.assertTrue(expected.issubset(formulas))

    def test_evaluate_ast(self):
        p = ExpressionNode(operation='variable', variable='P')
        q = ExpressionNode(operation='variable', variable='Q')
        r = ExpressionNode(operation='variable', variable='R')
        imp = ExpressionNode(operation='implication', lhs=p, rhs=q)
        neg_r = ExpressionNode(operation='negation', lhs=r)
        and_node = ExpressionNode(operation='conjunction', lhs=imp, rhs=neg_r)
        env = {'P': False, 'Q': False, 'R': False}
        self.assertTrue(evaluate_ast(and_node, env))
        env['R'] = True
        self.assertFalse(evaluate_ast(and_node, env))

    # Новые тесты для валидации
    def test_mark_subtrees_invalid_root(self):
        with self.assertRaises(TypeError):
            mark_subtrees("not a node")
        with self.assertRaises(TypeError):
            mark_subtrees(None)

    def test_mark_subtrees_invalid_variable(self):
        node = ExpressionNode(operation='variable')
        with self.assertRaises(ValueError):
            mark_subtrees(node)

        node = ExpressionNode(operation='variable', variable=123)
        with self.assertRaises(ValueError):
            mark_subtrees(node)

    def test_mark_subtrees_invalid_negation(self):
        node = ExpressionNode(operation='negation')
        with self.assertRaises(ValueError):
            mark_subtrees(node)

    def test_mark_subtrees_invalid_binary_op(self):
        p = ExpressionNode(operation='variable', variable='P')
        node = ExpressionNode(operation='conjunction', lhs=p)
        with self.assertRaises(ValueError):
            mark_subtrees(node)

    def test_mark_subtrees_unknown_operation(self):
        node = ExpressionNode(operation='unknown')
        with self.assertRaises(ValueError):
            mark_subtrees(node)

    def test_calculate_depth_invalid_node(self):
        with self.assertRaises(TypeError):
            calculate_depth("not a node")
        with self.assertRaises(TypeError):
            calculate_depth(None)

    def test_calculate_depth_invalid_negation(self):
        node = ExpressionNode(operation='negation')
        with self.assertRaises(ValueError):
            calculate_depth(node)

    def test_calculate_depth_invalid_binary_op(self):
        p = ExpressionNode(operation='variable', variable='P')
        node = ExpressionNode(operation='conjunction', lhs=p)
        with self.assertRaises(ValueError):
            calculate_depth(node)

    def test_gather_subtrees_invalid_root(self):
        with self.assertRaises(TypeError):
            gather_subtrees("not a node")
        with self.assertRaises(TypeError):
            gather_subtrees(None)

    def test_gather_subtrees_invalid_node_type(self):
        class FakeNode:
            pass

        root = FakeNode()
        with self.assertRaises(TypeError):
            gather_subtrees(root)

    def test_gather_subtrees_invalid_variable(self):
        node = ExpressionNode(operation='variable')
        with self.assertRaises(ValueError):
            gather_subtrees(node)

    def test_evaluate_ast_invalid_node(self):
        with self.assertRaises(TypeError):
            evaluate_ast("not a node", {})
        with self.assertRaises(TypeError):
            evaluate_ast(None, {})

    def test_evaluate_ast_invalid_env(self):
        node = ExpressionNode(operation='variable', variable='P')
        with self.assertRaises(TypeError):
            evaluate_ast(node, "not a dict")
        with self.assertRaises(TypeError):
            evaluate_ast(node, None)

    def test_evaluate_ast_missing_variable(self):
        node = ExpressionNode(operation='variable', variable='P')
        with self.assertRaises(ValueError):
            evaluate_ast(node, {})

    def test_evaluate_ast_invalid_variable_node(self):
        node = ExpressionNode(operation='variable')
        with self.assertRaises(ValueError):
            evaluate_ast(node, {'P': True})

    def test_evaluate_ast_invalid_negation(self):
        node = ExpressionNode(operation='negation')
        with self.assertRaises(ValueError):
            evaluate_ast(node, {})

    def test_evaluate_ast_invalid_binary_op(self):
        p = ExpressionNode(operation='variable', variable='P')
        node = ExpressionNode(operation='conjunction', lhs=p)
        with self.assertRaises(ValueError):
            evaluate_ast(node, {'P': True})


