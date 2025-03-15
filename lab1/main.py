from run import *


def main():
    print("Введите два целых числа для анализа")

    # Ввод первого числа
    while True:
        try:
            num1 = int(input("Первое число: "))
            break
        except ValueError:
            print("Ошибка! Введите целое число")

    # Ввод второго числа
    while True:
        try:
            num2 = int(input("Второе число: "))
            break
        except ValueError:
            print("Ошибка! Введите целое число")

    bit_length = 8
    print(f"\nБитовая длина представления: {bit_length} бит")

    # Вывод представлений для первого числа
    print("\nПредставления первого числа:")
    if num1 > 0:
        print(f"Прямой код: {get_positive_code(num1, bit_length)}")
    else:
        print(f"Прямой код: {get_negative_code(num1, bit_length)}")
    print(f"Обратный код: {get_reverse_code(num1, bit_length)}")
    print(f"Дополнительный код: {get_additional_code(num1, bit_length)}")

    # Вывод представлений для второго числа
    print("\nПредставления второго числа:")
    if num2 > 0:
        print(f"Прямой код: {get_positive_code(num2, bit_length)}")
    else:
        print(f"Прямой код: {get_negative_code(num2, bit_length)}")
    print(f"Обратный код: {get_reverse_code(num2, bit_length)}")
    print(f"Дополнительный код: {get_additional_code(num2, bit_length)}")

    # Арифметические операции
    print("\nРезультаты арифметических операций:")

    # Сложение
    sum_result = add_in_additional_code(num1, num2, bit_length)
    print(f"\nСложение ({num1} + {num2}):")
    print(f"Дополнительный код: {sum_result}")
    print(f"Десятичный результат: {twos_complement_to_decimal(sum_result)}")

    # Вычитание
    sub_result = subtract_in_additional_code(num1, num2, bit_length)
    print(f"\nВычитание ({num1} - {num2}):")
    print(f"Дополнительный код: {sub_result}")
    print(f"Десятичный результат: {twos_complement_to_decimal(sub_result)}")

    print("\nТестирование умножения в прямом коде:")
    mul_code = multiply_in_direct_code(num1, num2, 8)

    def direct_code_to_decimal(direct_str):
        bit_length = len(direct_str)
        if direct_str[0] == '0':
            return binary_to_decimal(direct_str[1:])
        else:
            return -binary_to_decimal(direct_str[1:])

    print(f"Умножение {num1} и {num2}:")
    print(f"Результат (bin): {mul_code}")
    print(f"Результат (dec): {direct_code_to_decimal(mul_code)}")

    if num2 == 0:
        print("\nДеление на ноль невозможно!")
    else:
        div_result, div_dec = divide_in_direct_code(num1, num2, 5, bit_length)
        print(f"\nДеление ({num1} / {num2}):")
        print(f"Прямой код: {div_result}")
        print(f"Десятичный результат: {div_dec:.5f}")

    print("\nТестирование сложения чисел с плавающей точкой по IEEE-754:")
    try:
        a = float(input("Введите первое число (например, 3.3): "))
        b = float(input("Введите второе число (например, 4.9): "))
    except Exception as e:
        print("Ошибка ввода:", e)
        exit(1)

    ieee_a = convert_float_to_ieee754(a)
    ieee_b = convert_float_to_ieee754(b)

    print("\nПредставление чисел в IEEE-754 (32 бит):")
    print("A =", a, "->", ieee_a)
    print("B =", b, "->", ieee_b)

    ieee_result = add_ieee754(ieee_a, ieee_b)
    print("\nРезультат сложения в формате IEEE-754 (32 бит):")
    print(ieee_result)

    dec_result = ieee754_to_decimal(ieee_result)
    print("\nРезультат сложения (десятичное значение):")
    print(dec_result)


if __name__ == "__main__":
    main()
