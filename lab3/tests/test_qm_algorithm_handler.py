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
        # minterms for f(A,B): A'B + AB => terms [1,3]
        primes = compute_prime_implicants([1,3], 2, ['A','B'], is_dnf=True)
        # Prime implicant after merging is '-1'
        self.assertEqual(primes, ['-1'])

class TestIdentifyEssentialImplicants(unittest.TestCase):
    def test_dnf_returns_same(self):
        primes = ['01','11']
        essential = identify_essential_implicants(primes, [1,3], 2, ['A','B'], is_dnf=True)
        self.assertEqual(essential, primes)

    def test_cnf_filters(self):
        # In CNF, choose implicants not subset of others
        primes = ['0-','-1','11']
        essential = identify_essential_implicants(primes, [0,1,3], 2, ['A','B'], is_dnf=False)
        self.assertIn('11', essential)
        self.assertNotIn('-1', essential)

class TestOptimizeDNFAndCNF(unittest.TestCase):
    def test_optimize_dnf(self):
        # f = A'B + AB for minterms [1,3]
        res = optimize_dnf([1,3], 2, ['A','B'])
        # After minimization simplest implicant is B
        self.assertEqual(res, '(B)')

    def test_optimize_cnf(self):
        # maxterms for g = (A+¬B)(¬A+B) => indices [0,2]
        res = optimize_cnf([0,2], 2, ['A','B'])
        # After minimization simplest clause is B
        self.assertEqual(res, '(B)')

class TestCoverageAndDisplay(unittest.TestCase):
    def test_construct_coverage_table(self):
        primes = ['01','11']
        table = construct_coverage_table(primes, [1,3], 2, ['A','B'], is_dnf=True)
        # '01' covers minterm 1, '11' covers minterm 3
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
        # Should include DNF literals conjunction form
        self.assertIn('(¬A∧B)', output)
        self.assertIn('(A∧B)', output)

class TestConvertTermToClause(unittest.TestCase):
    def test_for_cnf(self):
        clause = convert_term_to_clause(2, ['A','B','C'], for_cnf=True)
        # 2 -> '010' -> (A∨¬B∨C)
        self.assertEqual(clause, '(A∨¬B∨C)')
    def test_for_dnf(self):
        clause = convert_term_to_clause(5, ['X','Y','Z'], for_cnf=False)
        # 5 -> '101' -> (X∧¬Y∧Z)
        self.assertEqual(clause, '(X∧¬Y∧Z)')

class TestTabularMethodProcessor(unittest.TestCase):
    def test_returns_primes(self):
        primes = tabular_method_processor([1,3], 2, ['A','B'], is_dnf=True)
        # After merging, only '-1' remains
        self.assertEqual(primes, ['-1'])

if __name__ == '__main__':
    unittest.main()
