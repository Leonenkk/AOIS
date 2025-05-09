import unittest
import io
import sys

from lab3.views.truth_table_analyzer import compute_truth_table

class TestComputeTruthTable(unittest.TestCase):
    def test_single_variable(self):
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            result = compute_truth_table('p')
        finally:
            sys.stdout = sys_stdout
        self.assertEqual(result['variables'], ['p'])
        self.assertEqual(result['component_count'], 1)
        self.assertEqual(result['minimal_terms'], [1])
        self.assertEqual(result['maximal_terms'], [0])
        self.assertEqual(result['dnf_formula'], '(p)')
        # Code outputs CNF as '(P)' (single clause with the variable itself)
        self.assertEqual(result['cnf_formula'], '(p)')
        self.assertEqual(result['index_value'], 1)
        self.assertEqual(result['binary_pattern'], '01')

    def test_conjunction(self):
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            result = compute_truth_table('p & q')
        finally:
            sys.stdout = sys_stdout
        self.assertEqual(result['variables'], ['p', 'q'])
        self.assertEqual(result['component_count'], 2)
        self.assertEqual(result['minimal_terms'], [3])
        self.assertEqual(result['maximal_terms'], [0, 1, 2])
        self.assertEqual(result['dnf_formula'], '(p∧q)')
        # Code returns full CNF as product of sums
        expected_cnf = '(p∨q) ∧ (p∨¬q) ∧ (¬p∨q)'
        self.assertEqual(result['cnf_formula'], expected_cnf)
        self.assertEqual(result['index_value'], 1)
        self.assertEqual(result['binary_pattern'], '0001')
