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

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            convert_number_to_bits(-1, 4)  # Отрицательное число
        with self.assertRaises(ValueError):
            convert_number_to_bits(5, 0)  # Нулевая длина
        with self.assertRaises(ValueError):
            convert_number_to_bits(8, 3)  # Число превышает максимальное
        with self.assertRaises(ValueError):
            convert_number_to_bits("5", 3)  # Неправильный тип числа
        with self.assertRaises(ValueError):
            convert_number_to_bits(5, "3")  # Неправильный тип длины

class TestMergeImplicants(unittest.TestCase):
    def test_merge_adjacent(self):
        self.assertEqual(merge_implicants('01', '11'), '-1')
        self.assertEqual(merge_implicants('0-', '1-'), '--')

    def test_merge_non_adjacent(self):
        self.assertIsNone(merge_implicants('00', '11'))
        self.assertIsNone(merge_implicants('0-', '-1'))

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            merge_implicants(123, '11')  # Неправильный тип первого терма
        with self.assertRaises(TypeError):
            merge_implicants('01', 456)  # Неправильный тип второго терма
        with self.assertRaises(ValueError):
            merge_implicants('01', '111')  # Разная длина
        with self.assertRaises(ValueError):
            merge_implicants('0A', '11')  # Недопустимый символ
        with self.assertRaises(ValueError):
            merge_implicants('01', '1B')  # Недопустимый символ

class TestTranslateBinaryToLiterals(unittest.TestCase):
    def test_conjunctive(self):
        self.assertEqual(translate_binary_to_literals('10', ['A','B'], use_conjunction=True), 'A∧¬B')
        self.assertEqual(translate_binary_to_literals('-0', ['A','B'], use_conjunction=True), '¬B')
        self.assertEqual(translate_binary_to_literals('--', ['A','B'], use_conjunction=True), '1')

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            translate_binary_to_literals(123, ['A','B'], True)  # Неправильный тип шаблона
        with self.assertRaises(TypeError):
            translate_binary_to_literals('10', 'AB', True)  # Неправильный тип переменных
        with self.assertRaises(ValueError):
            translate_binary_to_literals('102', ['A','B'], True)  # Недопустимый символ
        with self.assertRaises(ValueError):
            translate_binary_to_literals('10', ['A',123], True)  # Неправильный тип переменной
        with self.assertRaises(ValueError):
            translate_binary_to_literals('100', ['A','B'], True)  # Несоответствие длины


    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            extract_literals_from_pattern('12-', ['A','B','C'], True)  # Недопустимый символ
        with self.assertRaises(ValueError):
            extract_literals_from_pattern('10', ['A','B','C'], True)  # Несоответствие длины

class TestIsImplicantCoveringTerm(unittest.TestCase):
    def test_covering(self):
        self.assertTrue(is_implicant_covering_term('-1', '01'))
        self.assertTrue(is_implicant_covering_term('--', '11'))
        self.assertFalse(is_implicant_covering_term('0-', '11'))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            is_implicant_covering_term('1A', '01')  # Недопустимый символ
        with self.assertRaises(ValueError):
            is_implicant_covering_term('--', '1A')  # Недопустимый символ

class TestPruneRedundantImplicants(unittest.TestCase):
    def test_prune(self):
        primes = ['01','11','-1']
        minterms = [1,3]
        result = prune_redundant_implicants(primes, minterms, bit_count=2)
        self.assertEqual(result, ['-1'])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            prune_redundant_implicants([], [1,3], 2)  # Пустой список импликантов
        with self.assertRaises(ValueError):
            prune_redundant_implicants(['01','11'], [], 2)  # Пустой список минтермов
        with self.assertRaises(ValueError):
            prune_redundant_implicants(['01','11'], [1,3], 0)  # Нулевая длина бит

class TestConsolidateImplicants(unittest.TestCase):
    def test_consolidate(self):
        primes = ['-1','11']
        vars = ['A','B']
        result = consolidate_implicants(primes, vars, is_conjunctive=True)
        self.assertEqual(result, ['-1'])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            consolidate_implicants([], ['A','B'], True)  # Пустой список импликантов
        with self.assertRaises(ValueError):
            consolidate_implicants(['-1','11'], [], True)  # Пустой список переменных
        with self.assertRaises(ValueError):
            consolidate_implicants(['-1','111'], ['A','B'], True)  # Несоответствие длины
