import unittest
from run import *

class TestBinaryArithmetic(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(5, 8), "00000101")
        self.assertEqual(decimal_to_binary(0, 8), "00000000")
        self.assertEqual(decimal_to_binary(15, 8), "00001111")

    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal("00000101"), 5)
        self.assertEqual(binary_to_decimal("00001111"), 15)

    def test_get_positive_code(self):
        self.assertEqual(get_positive_code(5, 8), "00000101")

    def test_get_negative_code(self):
        self.assertEqual(get_negative_code(-5, 8), "10000101")

    def test_get_reverse_code(self):
        self.assertEqual(get_reverse_code(-5, 8), "11111010")

    def test_get_additional_code(self):
        self.assertEqual(get_additional_code(-5, 8), "11111011")
        self.assertEqual(get_additional_code(5, 8), "00000101")

    def test_add_in_additional_code(self):
        sum_code = add_in_additional_code(5, -3, 8)
        self.assertEqual(twos_complement_to_decimal(sum_code), 2)

    def test_subtract_in_additional_code(self):
        sub_code = subtract_in_additional_code(2, 3, 8)
        self.assertEqual(twos_complement_to_decimal(sub_code), -1)

    def test_multiply_in_direct_code(self):
        mul_code = multiply_in_direct_code(5, -3, 8)

        def direct_code_to_decimal(direct_str):
            if direct_str[0] == '0':
                return binary_to_decimal(direct_str[1:])
            else:
                return -binary_to_decimal(direct_str[1:])

        self.assertEqual(direct_code_to_decimal(mul_code), -15)

    def test_divide_in_direct_code(self):
        div_bin, div_dec = divide_in_direct_code(7, -3, precision=5, int_bit_length=8)
        self.assertAlmostEqual(div_dec, -2.3125, places=3)


class TestIEEE754Functions(unittest.TestCase):
    def test_convert_and_revert(self):
        test_values = [1.0, 3.3, 4.9, 0.15625, 123.456]
        for value in test_values:
            ieee = convert_float_to_ieee754(value)
            dec = ieee754_to_decimal(ieee)
            self.assertAlmostEqual(value, dec, places=4, msg=f"Не сходится для {value}")

    def test_addition(self):
        a = 3.3
        b = 4.9
        ieee_a = convert_float_to_ieee754(a)
        ieee_b = convert_float_to_ieee754(b)
        ieee_sum = add_ieee754(ieee_a, ieee_b)
        dec_sum = ieee754_to_decimal(ieee_sum)
        expected_sum = a + b
        self.assertAlmostEqual(dec_sum, expected_sum, places=4,
                               msg=f"Сумма {a} + {b} должна быть ≈ {expected_sum}, получено {dec_sum}")

    def test_ieee_format(self):
        a = 3.3
        ieee = convert_float_to_ieee754(a)
        self.assertEqual(len(ieee), 32, msg="Представление должно состоять из 32 бит")
        self.assertTrue(all(bit in "01" for bit in ieee),
                        msg="Строка должна содержать только символы '0' и '1'")
