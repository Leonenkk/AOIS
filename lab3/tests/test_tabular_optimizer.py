import unittest
import io
import sys

from lab3.views.tabular_optimizer import (
    optimize_tabular_dnf,
    optimize_tabular_cnf,
    display_kmap
)

class TestQMAlgorithmHandler(unittest.TestCase):
    def test_optimize_tabular_dnf(self):
        # For f = A'B + AB => minterms [1,3]
        result = optimize_tabular_dnf([1, 3], 2, ['A', 'B'])
        # After tabular minimization, simplest implicant is B
        self.assertEqual(result, '(B)')

    def test_optimize_tabular_cnf(self):
        # For g = (A+¬B)(¬A+B) => maxterms [0,2]
        result = optimize_tabular_cnf([0, 2], 2, ['A', 'B'])
        # After tabular minimization, simplest clause is B
        self.assertEqual(result, '(B)')

    def test_display_kmap_without_labels(self):
        # grid only
        grid = [['0', '1'], ['1', '0']]
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            display_kmap(grid)
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        # Should print two rows of '0  1' and '1  0'
        self.assertIn('0', output)
        self.assertIn('1', output)
        # Each row separated by newline
        self.assertTrue(output.count('\n') >= 2)

    def test_display_kmap_with_labels(self):
        grid = [['X', 'Y'], ['Z', 'W']]
        row_labels = ['R0', 'R1']
        col_labels = ['C0', 'C1']
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            display_kmap(grid, row_labels=row_labels, col_labels=col_labels)
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        # Header should include column labels
        self.assertIn('C0', output)
        self.assertIn('C1', output)
        # Rows should include row labels and grid content
        self.assertIn('R0', output)
        self.assertIn('R1', output)
        self.assertIn('X', output)
        self.assertIn('W', output)

if __name__ == '__main__':
    unittest.main()
