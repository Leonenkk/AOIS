def decimal_to_binary(n, bit_length=None):
    """Перевод неотрицательного целого числа в двоичную строку (без знака)"""
    if n == 0:
        return '0'.zfill(bit_length) if bit_length else '0'
    binary = []
    while n > 0:
        binary.append(str(n % 2))
        n //= 2
    binary_str = ''.join(reversed(binary))
    if bit_length:
        binary_str = binary_str.zfill(bit_length)
    return binary_str


def binary_to_decimal(binary_str):
    """Перевод двоичной строки (представляющей неотрицательное число) в десятичное"""
    return int(binary_str, 2)


def twos_complement_to_decimal(binary_str):
    """Преобразование числа в дополнительном (двоичном) коде (как строка) в знаковое целое"""
    bit_length = len(binary_str)
    unsigned_val = binary_to_decimal(binary_str)
    if binary_str[0] == '0':
        return unsigned_val
    else:
        return unsigned_val - (1 << bit_length)


def get_positive_code(n, bit_length):
    """Прямой (знаковый) код для положительного числа.
       bit_length включает бит знака (старший бит = 0)"""
    binary_str = decimal_to_binary(n, bit_length - 1)
    return '0' + binary_str


def get_negative_code(n, bit_length):
    """Прямой (знаковый) код для отрицательного числа.
       Представление: старший бит = 1, а остальные – двоичное представление модуля,
       дополненное нулями до (bit_length-1) разрядов."""
    binary_str = decimal_to_binary(abs(n), bit_length - 1)
    return '1' + binary_str


def get_reverse_code(n, bit_length):
    """Обратный код.
       Для положительных чисел – тот же прямой код,
       для отрицательных – инвертируем все разряды величины (но сохраняем знак = 1)."""
    if n >= 0:
        return get_positive_code(n, bit_length)
    pos_code = decimal_to_binary(abs(n), bit_length - 1)
    pos_code = '0' + pos_code  # знак 0
    inverted = ''.join('1' if bit == '0' else '0' for bit in pos_code[1:])
    return '1' + inverted


def get_additional_code(n, bit_length):
    """Дополнительный (двоичный) код.
       Для положительных чисел – прямой код;
       для отрицательных – обратный код плюс 1."""
    if n >= 0:
        return get_positive_code(n, bit_length)
    rev = get_reverse_code(n, bit_length)
    carry = 1
    additional = []
    for bit in reversed(rev):
        total = int(bit) + carry
        additional.append(str(total % 2))
        carry = total // 2
    result = ''.join(reversed(additional))
    return result[-bit_length:]


def add_in_additional_code(a, b, bit_length):
    """Сложение двух чисел в дополнительном коде с фиксированной длиной bit_length.
       Результат возвращается в виде двоичной строки (дополнительного кода).
       Для проверки десятичное значение получается с помощью twos_complement_to_decimal()."""
    a_code = get_additional_code(a, bit_length).zfill(bit_length)
    b_code = get_additional_code(b, bit_length).zfill(bit_length)
    result = []
    carry = 0
    for i in range(bit_length - 1, -1, -1):
        total = int(a_code[i]) + int(b_code[i]) + carry
        result.append(str(total % 2))
        carry = total // 2
    result_str = ''.join(reversed(result))
    # Если переполнение (выход за bit_length), отбросить старший разряд
    if len(result_str) > bit_length:
        result_str = result_str[-bit_length:]
    return result_str


def subtract_in_additional_code(a, b, bit_length):
    """Вычитание: a - b = a + (-b), все числа представлены в дополнительном коде"""
    return add_in_additional_code(a, -b, bit_length)


def multiply_in_direct_code(a, b, bit_length):
    """Умножение в прямом (знаковом) коде.
       Числа вводятся в десятичном формате, результат выводится как строка прямого кода.
       Если число отрицательное, знак кодируется установкой старшего бита в 1."""
    product = a * b
    if product >= 0:
        return get_positive_code(product, bit_length)
    else:
        return get_negative_code(product, bit_length)


def divide_in_direct_code(a, b, precision=5, int_bit_length=8):
    """Деление в прямом (знаковом) коде с точностью до precision двоичных разрядов дробной части.
       Для целой части используется int_bit_length (включая бит знака).
       Возвращает кортеж: (результат в двоичном виде, десятичное значение результата)."""
    if b == 0:
        return "Ошибка: деление на ноль", None
    sign = 1
    if a < 0:
        sign = -1
        a = abs(a)
    if b < 0:
        sign *= -1
        b = abs(b)
    quotient = a // b
    remainder = a % b
    quotient_bin = decimal_to_binary(quotient, int_bit_length - 1)
    if sign < 0:
        direct_quotient = '1' + quotient_bin
    else:
        direct_quotient = '0' + quotient_bin
    fractional_bits = ""
    for _ in range(precision):
        remainder *= 2
        digit = remainder // b
        fractional_bits += str(digit)
        remainder %= b
    result_bin = direct_quotient + "." + fractional_bits
    frac_val = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(fractional_bits))
    result_dec = sign * (quotient + frac_val)
    return result_bin, result_dec


def convert_float_to_ieee754(num):
    """
    Преобразование положительного десятичного числа с плавающей точкой (num)
    в 32-битовое представление IEEE-754 по стандарту.
    Реализация полностью «с нуля»: разделение на целую и дробную части,
    перевод каждой части в двоичный вид, нормализация, вычисление экспоненты и формирование мантиссы.
    """
    int_part = int(num)
    frac_part = num - int(num)
    bin_int = ""
    if int_part == 0:
        bin_int = "0"
    else:
        temp = int_part
        while temp > 0:
            rem = temp % 2
            bin_int = str(rem) + bin_int
            temp = temp // 2
    bin_frac = ""
    temp_frac = frac_part
    for _ in range(30):
        temp_frac = temp_frac * 2
        if temp_frac >= 1:
            bin_frac += "1"
            temp_frac = temp_frac - 1
        else:
            bin_frac += "0"
    # Если целая часть не равна нулю: число представляется как 1.xxx * 2^(len(bin_int)-1)
    if bin_int != "0":
        exponent = len(bin_int) - 1
        mantissa = (bin_int[1:] + bin_frac)[:23]
        if len(mantissa) < 23:
            mantissa = mantissa + "0" * (23 - len(mantissa))
    else:
        index = 0
        while index < len(bin_frac) and bin_frac[index] == "0":
            index += 1
        if index == len(bin_frac):
            exponent = -127
            mantissa = "0" * 23
        else:
            exponent = -(index + 1)
            mantissa = bin_frac[index + 1:index + 1 + 23]
            if len(mantissa) < 23:
                mantissa = mantissa + "0" * (23 - len(mantissa))
    exp_val = exponent + 127
    exp_bits = ""
    temp_exp = exp_val
    for i in range(8):
        bit = temp_exp % 2
        exp_bits = str(bit) + exp_bits
        temp_exp = temp_exp // 2
    ieee = "0" + exp_bits + mantissa
    return ieee


def ieee754_to_decimal(ieee):
    """
    Преобразование 32-битового представления IEEE-754 (строка)
    в десятичное число. Реализовано вручную: извлечение экспоненты и мантиссы,
    восстановление неявной единицы, вычисление значения.
    """
    sign = 1 if ieee[0] == "0" else -1
    exponent = 0
    for bit in ieee[1:9]:
        exponent = exponent * 2 + (1 if bit == "1" else 0)
    exponent = exponent - 127
    mantissa = 1.0
    frac_bits = ieee[9:]
    power = 0.5
    for bit in frac_bits:
        if bit == "1":
            mantissa += power
        power /= 2
    return sign * mantissa * (2 ** exponent)


def add_ieee754(bin1, bin2):
    exp1 = 0
    for bit in bin1[1:9]:
        exp1 = exp1 * 2 + (1 if bit == "1" else 0)
    exp2 = 0
    for bit in bin2[1:9]:
        exp2 = exp2 * 2 + (1 if bit == "1" else 0)
    mant1 = 0
    for bit in ("1" + bin1[9:]):
        mant1 = mant1 * 2 + (1 if bit == "1" else 0)
    mant2 = 0
    for bit in ("1" + bin2[9:]):
        mant2 = mant2 * 2 + (1 if bit == "1" else 0)
    if exp1 > exp2:
        diff = exp1 - exp2
        mant2 = mant2 >> diff
        exp = exp1
    else:
        diff = exp2 - exp1
        mant1 = mant1 >> diff
        exp = exp2
    sum_mant = mant1 + mant2
    if sum_mant >= (1 << 24):
        sum_mant = sum_mant >> 1
        exp += 1
    frac = sum_mant - (1 << 23)
    frac_str = ""
    for i in range(23):
        bit = (frac >> (22 - i)) & 1
        frac_str += "1" if bit == 1 else "0"
    exp_str = ""
    temp = exp
    for i in range(8):
        exp_str = ("1" if (temp % 2) == 1 else "0") + exp_str
        temp = temp // 2
    return "0" + exp_str + frac_str


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
    print(f"Прямой код: {get_negative_code(num1, bit_length)}")
    print(f"Обратный код: {get_reverse_code(num1, bit_length)}")
    print(f"Дополнительный код: {get_additional_code(num1, bit_length)}")

    # Вывод представлений для второго числа
    print("\nПредставления второго числа:")
    print(f"Прямой код: {get_positive_code(num2, bit_length)}")
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
    mul_code = multiply_in_direct_code(num1,num2, 8)
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