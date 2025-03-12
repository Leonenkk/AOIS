from main import *
import unittest


class TestLogicFunctions(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(5, 4), '0101')
        self.assertEqual(decimal_to_binary(0, 3), '000')
        self.assertEqual(decimal_to_binary(7, 3), '111')
        self.assertEqual(decimal_to_binary(42, 8), '00101010')

    def test_parse_expression(self):
        # Проверка извлечения переменных и замены операторов
        self.assertEqual(parse_expression('(a∨b)∧¬c'), (['a', 'b', 'c'], '(a|b)&!c'))
        self.assertEqual(parse_expression('a→b∼c'), (['a', 'b', 'c'], 'a>b=c'))
        self.assertEqual(parse_expression('a ∧ (b | c)'), (['a', 'b', 'c'], 'a&(b|c)'))

    def test_evaluate_postfix(self):
        # Тест для: a | b
        postfix = ['a', 'b', '|']
        values = {'a': 1, 'b': 0}
        self.assertEqual(evaluate_postfix(postfix, values), 1)

        # Тест для: !a & b
        postfix = ['a', '!', 'b', '&']
        values = {'a': 1, 'b': 1}
        self.assertEqual(evaluate_postfix(postfix, values), 0)

    def test_shunting_yard(self):
        # Простые выражения
        self.assertEqual(shunting_yard('a|b'), ['a', 'b', '|'])
        self.assertEqual(shunting_yard('!a&b'), ['a', '!', 'b', '&'])

        # Со скобками
        self.assertEqual(shunting_yard('(a|b)&c'), ['a', 'b', '|', 'c', '&'])

        # С приоритетами операторов
        self.assertEqual(shunting_yard('a|b&c'), ['a', 'b', 'c', '&', '|'])

    def test_generate_truth_table(self):
        variables = ['a']
        postfix = ['a', '!']  # Функция !a
        table = generate_truth_table(variables, postfix)
        self.assertEqual(table, [
            ([0], 1),
            ([1], 0)
        ])

    def test_build_forms(self):
        # Тест для функции: a
        table = [([0], 0), ([1], 1)]
        forms = build_forms(table, ['a'])
        self.assertEqual(forms['sdnf'], '(a)')
        self.assertEqual(forms['sknf'], '(a)')
        self.assertEqual(forms['index'], '1 (01)')  # 1 в двоичном виде с длиной 2

    def test_full_flow(self):
        # Тест полного цикла для выражения: a
        variables, parsed_expr = parse_expression('a')
        postfix = shunting_yard(parsed_expr)
        table = generate_truth_table(variables, postfix)
        forms = build_forms(table, variables)

        self.assertEqual(forms['sdnf'], '(a)')
        self.assertEqual(forms['numeric_sdnf'], '1')
        self.assertEqual(forms['index'], '1 (01)')


if __name__ == '__main__':
    unittest.main()