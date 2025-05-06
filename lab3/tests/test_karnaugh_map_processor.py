import unittest
import io
import sys

from lab3.views.karnaugh_map_processor import (
    generate_gray_sequence,
    _convert_to_binary_terms,
    _combine_terms_pair,
    _identify_prime_implicants,
    _is_implicant_covering,
    _select_essential_implicants,
    optimize_kmap,
    display_kmap_table,
)

class TestGraySequence(unittest.TestCase):
    def test_generate_gray_sequence_length_2(self):
        self.assertEqual(generate_gray_sequence(2), [0, 1, 3, 2])

    def test_generate_gray_sequence_length_3(self):
        expected = [0, 1, 3, 2, 6, 7, 5, 4]
        self.assertEqual(generate_gray_sequence(3), expected)

class TestConvertToBinaryTerms(unittest.TestCase):
    def test_convert_single_term(self):
        self.assertEqual(_convert_to_binary_terms([2], 2), [(1, 0)])

    def test_convert_multiple_terms(self):
        self.assertEqual(
            _convert_to_binary_terms([0, 1, 3], 2),
            [(0, 0), (0, 1), (1, 1)]
        )

class TestCombineTermsPair(unittest.TestCase):
    def test_combine_adjacent(self):
        a = (0, 0)
        b = (0, 1)
        self.assertEqual(_combine_terms_pair(a, b), (0, '-'))

    def test_combine_non_adjacent(self):
        self.assertIsNone(_combine_terms_pair((0, 0), (1, 1)))

class TestPrimeImplicants(unittest.TestCase):
    def test_identify_prime_implicants_simple(self):
        bins = [(0, 0), (0, 1), (1, 1)]
        primes = _identify_prime_implicants(bins, 2)
        # Expect only combined implicants (0,'-') and ('-',1)
        self.assertEqual(primes, {(0, '-'), ('-', 1)})

class TestImplicantCoverage(unittest.TestCase):
    def test_is_implicant_covering(self):
        imp = ('-', 1)
        mt = (0, 1)
        self.assertTrue(_is_implicant_covering(imp, mt))
        self.assertFalse(_is_implicant_covering((1, 0), (0, 0)))

class TestSelectEssentialImplicants(unittest.TestCase):
    def test_select_essential(self):
        primes = {(0, '-'), ('-', 1), (1, 1)}
        minterms = [(0, 1), (1, 1)]
        essentials = _select_essential_implicants(primes, minterms)
        # Ensure each minterm is covered by at least one essential implicant
        for mt in minterms:
            self.assertTrue(any(_is_implicant_covering(imp, mt) for imp in essentials))

class TestOptimizeKmap(unittest.TestCase):
    def test_optimize_conjunctive(self):
        terms = [1, 3]
        names = ['A', 'B']
        res = optimize_kmap(terms, 2, names, use_conjunctive=True)
        self.assertEqual(res, ['(B)'])

    def test_optimize_disjunctive(self):
        terms = [0, 2]
        names = ['A', 'B']
        res = optimize_kmap(terms, 2, names, use_conjunctive=False)
        self.assertTrue(len(res) >= 1)

class TestDisplayKmapTable(unittest.TestCase):
    def test_display_table_output(self):
        buf = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buf
        try:
            display_kmap_table([1, 3], 2, ['A', 'B'], use_conjunctive=True)
        finally:
            sys.stdout = sys_stdout
        output = buf.getvalue()
        # Should contain header and values
        self.assertIn('A \\ B', output)
        self.assertIn('1', output)
        self.assertIn('0', output)

if __name__ == '__main__':
    unittest.main()