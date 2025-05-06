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
        # For a single negation of variable, no parentheses
        self.assertEqual(neg.formula, '¬Q')

    def test_mark_subtrees_negation_complex(self):
        # ¬(P ∨ R)
        p = ExpressionNode(operation='variable', variable='P')
        r = ExpressionNode(operation='variable', variable='R')
        disj = ExpressionNode(operation='disjunction', lhs=p, rhs=r)
        neg = ExpressionNode(operation='negation', lhs=disj)
        mark_subtrees(neg)
        self.assertEqual(disj.formula, 'P∨R')
        self.assertEqual(neg.formula, '¬(P∨R)')

    def test_mark_subtrees_binary_ops(self):
        # (P ∧ Q) → R
        p = ExpressionNode(operation='variable', variable='P')
        q = ExpressionNode(operation='variable', variable='Q')
        r = ExpressionNode(operation='variable', variable='R')
        conj = ExpressionNode(operation='conjunction', lhs=p, rhs=q)
        imp = ExpressionNode(operation='implication', lhs=conj, rhs=r)
        mark_subtrees(imp)
        self.assertEqual(conj.formula, 'P∧Q')
        # Implication should wrap left if needed
        self.assertEqual(imp.formula, 'P∧Q→R')

    def test_calculate_depth(self):
        # Depth of P is 1
        p = ExpressionNode(operation='variable', variable='P')
        self.assertEqual(calculate_depth(p), 1)
        # ¬P depth is 2
        neg = ExpressionNode(operation='negation', lhs=p)
        self.assertEqual(calculate_depth(neg), 2)
        # (P ∧ Q) ∧ R depth is 3
        q = ExpressionNode(operation='variable', variable='Q')
        conj1 = ExpressionNode(operation='conjunction', lhs=p, rhs=q)
        conj2 = ExpressionNode(operation='conjunction', lhs=conj1, rhs=ExpressionNode(operation='variable', variable='R'))
        self.assertEqual(calculate_depth(conj2), 3)

    def test_gather_subtrees(self):
        # Formula: (P ∧ Q) ∨ R
        p = ExpressionNode(operation='variable', variable='P')
        q = ExpressionNode(operation='variable', variable='Q')
        r = ExpressionNode(operation='variable', variable='R')
        conj = ExpressionNode(operation='conjunction', lhs=p, rhs=q)
        disj = ExpressionNode(operation='disjunction', lhs=conj, rhs=r)
        mark_subtrees(disj)
        subs = gather_subtrees(disj)
        # Expected formulas: 'P', 'Q', 'P∧Q', 'R', '(P∧Q)∨R' or 'P∨R' depending
        formulas = {node.formula for node in subs}
        expected = {'P', 'Q', 'P∧Q', 'R', 'P∧Q∨R'}
        self.assertTrue(expected.issubset(formulas))

    def test_evaluate_ast(self):
        # (P → Q) ∧ ¬R
        p = ExpressionNode(operation='variable', variable='P')
        q = ExpressionNode(operation='variable', variable='Q')
        r = ExpressionNode(operation='variable', variable='R')
        imp = ExpressionNode(operation='implication', lhs=p, rhs=q)
        neg_r = ExpressionNode(operation='negation', lhs=r)
        and_node = ExpressionNode(operation='conjunction', lhs=imp, rhs=neg_r)
        # True when P=False, Q=False, R=False
        env = {'P': False, 'Q': False, 'R': False}
        self.assertTrue(evaluate_ast(and_node, env))
        # False when R=True
        env['R'] = True
        self.assertFalse(evaluate_ast(and_node, env))

if __name__ == '__main__':
    unittest.main()
