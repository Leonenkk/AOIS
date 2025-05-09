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
        result = optimize_tabular_dnf([1, 3], 2, ['A', 'B'])
        self.assertEqual(result, '(B)')

    def test_optimize_tabular_cnf(self):
        result = optimize_tabular_cnf([0, 2], 2, ['A', 'B'])
        self.assertEqual(result, '(B)')

    def test_display_kmap_without_labels(self):
        grid = [['0', '1'], ['1', '0']]
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            display_kmap(grid)
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        self.assertIn('0', output)
        self.assertIn('1', output)
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
        self.assertIn('C0', output)
        self.assertIn('C1', output)
        self.assertIn('R0', output)
        self.assertIn('R1', output)
        self.assertIn('X', output)
        self.assertIn('W', output)

    # Новые тесты для валидации optimize_tabular_dnf
    def test_optimize_tabular_dnf_invalid_input(self):
        with self.assertRaises(TypeError):
            optimize_tabular_dnf("not a list", 2, ['A', 'B'])
        with self.assertRaises(ValueError):
            optimize_tabular_dnf([], 2, ['A', 'B'])  # Empty terms
        with self.assertRaises(ValueError):
            optimize_tabular_dnf([1, 3], 0, ['A', 'B'])  # Invalid var_count
        with self.assertRaises(ValueError):
            optimize_tabular_dnf([1, 3], 2, ['A'])  # Mismatched var_names
        with self.assertRaises(ValueError):
            optimize_tabular_dnf([1, 3], 2, [123, 'B'])  # Invalid var name

    # Новые тесты для валидации optimize_tabular_cnf
    def test_optimize_tabular_cnf_invalid_input(self):
        with self.assertRaises(TypeError):
            optimize_tabular_cnf("not a list", 2, ['A', 'B'])
        with self.assertRaises(ValueError):
            optimize_tabular_cnf([], 2, ['A', 'B'])  # Empty terms
        with self.assertRaises(ValueError):
            optimize_tabular_cnf([0, 2], 0, ['A', 'B'])  # Invalid var_count
        with self.assertRaises(ValueError):
            optimize_tabular_cnf([0, 2], 2, ['A'])  # Mismatched var_names
        with self.assertRaises(ValueError):
            optimize_tabular_cnf([0, 2], 2, ['A', 456])  # Invalid var name


    # Тесты для edge cases
    def test_optimize_tabular_dnf_single_term(self):
        result = optimize_tabular_dnf([1], 1, ['A'])
        self.assertEqual(result, '(A)')

    def test_optimize_tabular_cnf_single_term(self):
        result = optimize_tabular_cnf([0], 1, ['A'])
        self.assertEqual(result, '(A)')

    def test_display_kmap_single_cell(self):
        grid = [['X']]
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            display_kmap(grid)
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        self.assertIn('X', output)

if __name__ == '__main__':
    unittest.main()