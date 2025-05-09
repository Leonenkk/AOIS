import unittest
import io
import sys
from lab3.views.qm_algorithm_handler import (
    compute_prime_implicants,
    identify_essential_implicants,
    optimize_dnf,
    optimize_cnf,
    construct_coverage_table,
    display_coverage_table,
    convert_term_to_clause,
    tabular_method_processor
)

class TestComputePrimeImplicants(unittest.TestCase):
    def test_simple(self):
        primes = compute_prime_implicants([1,3], 2, ['A','B'], is_dnf=True)
        self.assertEqual(primes, ['-1'])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            compute_prime_implicants("not a list", 2, ['A','B'])
        with self.assertRaises(ValueError):
            compute_prime_implicants([1,3], 0, ['A','B'])  # Invalid var_count
        with self.assertRaises(ValueError):
            compute_prime_implicants([1,3], 2, ['A'])  # Mismatched var_names
        with self.assertRaises(ValueError):
            compute_prime_implicants([1,5], 2, ['A','B'])  # Term exceeds max value
        with self.assertRaises(ValueError):
            compute_prime_implicants([-1,3], 2, ['A','B'])  # Negative term

class TestIdentifyEssentialImplicants(unittest.TestCase):
    def test_dnf_returns_same(self):
        primes = ['01','11']
        essential = identify_essential_implicants(primes, [1,3], 2, ['A','B'], is_dnf=True)
        self.assertEqual(essential, primes)

    def test_cnf_filters(self):
        primes = ['0-','-1','11']
        essential = identify_essential_implicants(primes, [0,1,3], 2, ['A','B'], is_dnf=False)
        self.assertIn('11', essential)
        self.assertNotIn('-1', essential)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            identify_essential_implicants("not a list", [1,3], 2, ['A','B'])
        with self.assertRaises(TypeError):
            identify_essential_implicants(['01','11'], "not a list", 2, ['A','B'])
        with self.assertRaises(ValueError):
            identify_essential_implicants(['01','11'], [1,3], 0, ['A','B'])  # Invalid var_count
        with self.assertRaises(ValueError):
            identify_essential_implicants(['01','11'], [1,3], 2, ['A'])  # Mismatched var_names

class TestOptimizeDNFAndCNF(unittest.TestCase):
    def test_optimize_dnf(self):
        res = optimize_dnf([1,3], 2, ['A','B'])
        self.assertEqual(res, '(B)')

    def test_optimize_cnf(self):
        res = optimize_cnf([0,2], 2, ['A','B'])
        self.assertEqual(res, '(B)')

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            optimize_dnf("not a list", 2, ['A','B'])
        with self.assertRaises(ValueError):
            optimize_dnf([], 2, ['A','B'])  # Empty minterms
        with self.assertRaises(TypeError):
            optimize_cnf("not a list", 2, ['A','B'])
        with self.assertRaises(ValueError):
            optimize_cnf([], 2, ['A','B'])  # Empty maxterms

class TestCoverageAndDisplay(unittest.TestCase):
    def test_construct_coverage_table(self):
        primes = ['01','11']
        table = construct_coverage_table(primes, [1,3], 2, ['A','B'], is_dnf=True)
        self.assertEqual(table['01'], ['Х', '.'])
        self.assertEqual(table['11'], ['.', 'Х'])

    def test_display_coverage_table(self):
        primes = ['01','11']
        table = construct_coverage_table(primes, [1,3], 2, ['A','B'], is_dnf=True)
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            display_coverage_table(table, [1,3], ['A','B'], is_dnf=True)
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        self.assertIn('(¬A∧B)', output)
        self.assertIn('(A∧B)', output)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            construct_coverage_table("not a list", [1,3], 2, ['A','B'])
        with self.assertRaises(TypeError):
            display_coverage_table("not a dict", [1,3], ['A','B'])

class TestConvertTermToClause(unittest.TestCase):
    def test_for_cnf(self):
        clause = convert_term_to_clause(2, ['A','B','C'], for_cnf=True)
        self.assertEqual(clause, '(A∨¬B∨C)')

    def test_for_dnf(self):
        clause = convert_term_to_clause(5, ['X','Y','Z'], for_cnf=False)
        self.assertEqual(clause, '(X∧¬Y∧Z)')

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            convert_term_to_clause(-1, ['A','B'])  # Negative index
        with self.assertRaises(TypeError):
            convert_term_to_clause(1, "not a list")  # Invalid var_names
        with self.assertRaises(ValueError):
            convert_term_to_clause(1, [])  # Empty var_names

class TestTabularMethodProcessor(unittest.TestCase):
    def test_returns_primes(self):
        primes = tabular_method_processor([1,3], 2, ['A','B'], is_dnf=True)
        self.assertEqual(primes, ['-1'])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            tabular_method_processor("not a list", 2, ['A','B'])
        with self.assertRaises(ValueError):
            tabular_method_processor([1,3], 0, ['A','B'])  # Invalid var_count

