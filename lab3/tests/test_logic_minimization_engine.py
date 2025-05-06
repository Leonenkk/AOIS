import unittest

from lab3.views.logic_minimization_engine import (
    convert_number_to_bits,
    merge_implicants,
    translate_binary_to_literals,
    extract_literals_from_pattern,
    is_implicant_covering_term,
    prune_redundant_implicants,
    consolidate_implicants,
)

class TestConvertNumberToBits(unittest.TestCase):
    def test_zero_bits(self):
        self.assertEqual(convert_number_to_bits(0, 4), '0000')

    def test_nonzero_bits(self):
        self.assertEqual(convert_number_to_bits(5, 3), '101')

class TestMergeImplicants(unittest.TestCase):
    def test_merge_adjacent(self):
        self.assertEqual(merge_implicants('01', '11'), '-1')

    def test_merge_non_adjacent(self):
        self.assertIsNone(merge_implicants('00', '11'))

class TestTranslateBinaryToLiterals(unittest.TestCase):
    def test_conjunctive(self):
        # 10 -> A∧¬B
        self.assertEqual(translate_binary_to_literals('10', ['A','B'], use_conjunction=True), 'A∧¬B')

class TestPruneRedundantImplicants(unittest.TestCase):
    def test_prune(self):
        primes = ['01','11','-1']
        minterms = [1,3]
        result = prune_redundant_implicants(primes, minterms, bit_count=2)
        self.assertEqual(result, ['-1'])

class TestConsolidateImplicants(unittest.TestCase):
    def test_consolidate(self):
        primes = ['-1','11']
        vars = ['A','B']
        result = consolidate_implicants(primes, vars, is_conjunctive=True)
        self.assertEqual(result, ['-1'])

if __name__ == '__main__':
    unittest.main()
