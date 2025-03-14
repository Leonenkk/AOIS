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
    decimal = 0
    for i, bit in enumerate(reversed(binary_str)):
        decimal += int(bit) * (2 ** i)
    return decimal
    #return int(binary_str, 2)


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


def binary_add(a, b):
    """
    Сложение двух двоичных чисел, заданных в виде строк (без знака).
    Возвращает строку с результатом.
    """
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    carry = 0
    result = ""
    for i in range(max_len - 1, -1, -1):
        sum_bit = (1 if a[i] == '1' else 0) + (1 if b[i] == '1' else 0) + carry
        result = ('1' if sum_bit % 2 == 1 else '0') + result
        carry = 1 if sum_bit >= 2 else 0
    if carry:
        result = '1' + result
    return result


def binary_subtract(a, b):
    """
    Вычитание b из a (a >= b) для двоичных чисел в виде строк (без знака).
    Возвращает результат в виде строки.
    """
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    result = ""
    borrow = 0
    for i in range(max_len - 1, -1, -1):
        diff = (1 if a[i] == '1' else 0) - (1 if b[i] == '1' else 0) - borrow
        if diff < 0:
            diff += 2
            borrow = 1
        else:
            borrow = 0
        result = ('1' if diff == 1 else '0') + result
    result = result.lstrip('0')
    return result if result != "" else "0"


def binary_compare(a, b):
    """
    Сравнение двух двоичных чисел (без знака), заданных строками.
    Возвращает 1, если a > b, 0 если равны, -1 если a < b.
    """
    a = a.lstrip('0')
    b = b.lstrip('0')
    if len(a) > len(b):
        return 1
    elif len(a) < len(b):
        return -1
    else:
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0


def multiply_in_direct_code(a, b, bit_length):
    """
    Умножение двух чисел в прямом (знаковом) коде.
    """
    sign_a = '0' if a >= 0 else '1'
    sign_b = '0' if b >= 0 else '1'
    mag_a = decimal_to_binary(abs(a), bit_length - 1)
    mag_b = decimal_to_binary(abs(b), bit_length - 1)

    product = "0"
    for i in range(len(mag_b) - 1, -1, -1):
        if mag_b[i] == '1':
            partial = mag_a + "0" * (len(mag_b) - 1 - i)
            product = binary_add(product, partial)
    if len(product) > bit_length - 1:
        product = product[-(bit_length - 1):]
    else:
        product = product.zfill(bit_length - 1)

    result_sign = '0' if sign_a == sign_b else '1'
    return result_sign + product


def divide_in_direct_code(a, b, precision=5, int_bit_length=8):
    """деление в прямом коде"""
    if b == 0:
        return "Ошибка: деление на ноль", None

    result_sign = '0' if (a >= 0 and b > 0) or (a < 0 and b < 0) else '1'
    dividend = decimal_to_binary(abs(a))
    divisor = decimal_to_binary(abs(b))

    quotient = ""
    temp = ""
    for bit in dividend:
        temp += bit
        temp = temp.lstrip('0')
        if temp == "":
            temp = "0"
        if binary_compare(temp, divisor) >= 0:
            quotient += "1"
            temp = binary_subtract(temp, divisor)
        else:
            quotient += "0"
    quotient = quotient.lstrip('0')
    if quotient == "":
        quotient = "0"
    remainder = temp

    fractional = ""
    for _ in range(precision):
        remainder = remainder + "0"
        remainder = remainder.lstrip('0')
        if remainder == "":
            remainder = "0"
        if binary_compare(remainder, divisor) >= 0:
            fractional += "1"
            remainder = binary_subtract(remainder, divisor)
        else:
            fractional += "0"

    int_part = quotient.zfill(int_bit_length - 1)
    direct_int = result_sign + int_part
    final_result = direct_int + "." + fractional

    dec_int = binary_to_decimal(quotient) if quotient != "" else 0
    frac_val = 0
    for i, bit in enumerate(fractional):
        if bit == "1":
            frac_val += 1 / (2 ** (i + 1))
    dec_result = dec_int + frac_val
    if result_sign == '1':
        dec_result = -dec_result
    return final_result, dec_result


def convert_float_to_ieee754(num):
    """
    Преобразует десятичное число с плавающей точкой в 32-битовое представление IEEE-754.
    Для отрицательных чисел вычисляется представление для abs(num), а затем меняется знак
    (первый бит становится '1').
    """
    sign_bit = "0"
    if num < 0:
        sign_bit = "1"
        num = -num
    int_part = int(num)
    frac_part = num - int_part
    bin_int = ""
    if int_part == 0:
        bin_int = "0"
    else:
        temp = int_part
        while temp > 0:
            bin_int = str(temp % 2) + bin_int
            temp //= 2
    bin_frac = ""
    temp_frac = frac_part
    for _ in range(30):
        temp_frac *= 2
        if temp_frac >= 1:
            bin_frac += "1"
            temp_frac -= 1
        else:
            bin_frac += "0"
    if bin_int != "0":
        exponent = len(bin_int) - 1
        mantissa = (bin_int[1:] + bin_frac)[:23]
        mantissa = mantissa.ljust(23, "0")
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
            mantissa = mantissa.ljust(23, "0")
    exp_val = exponent + 127
    exp_bits = ""
    temp_exp = exp_val
    for _ in range(8):
        exp_bits = str(temp_exp % 2) + exp_bits
        temp_exp //= 2

    ieee = sign_bit + exp_bits + mantissa
    return ieee


def ieee754_to_decimal(ieee):
    """
    Преобразует 32-битовое представление IEEE-754 (строка) в десятичное число.
    Извлекается знак, экспонента и мантисса, затем вычисляется итоговое значение.
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
    """
    Складывает два числа, представленных в формате IEEE-754 (32 бита), с корректной обработкой знака.
    """
    sign1 = 0 if bin1[0] == '0' else 1
    sign2 = 0 if bin2[0] == '0' else 1

    exp1 = 0
    for bit in bin1[1:9]:
        exp1 = exp1 * 2 + (1 if bit == "1" else 0)
    exp2 = 0
    for bit in bin2[1:9]:
        exp2 = exp2 * 2 + (1 if bit == "1" else 0)

    mant1 = (1 << 23) + int(bin1[9:], 2)
    mant2 = (1 << 23) + int(bin2[9:], 2)
    exp = exp1
    if exp1 > exp2:
        shift = exp1 - exp2
        mant2 >>= shift
    elif exp2 > exp1:
        shift = exp2 - exp1
        mant1 >>= shift
        exp = exp2

    if sign1 == sign2:
        result_mant = mant1 + mant2
        result_sign = sign1
    else:
        if mant1 >= mant2:
            result_mant = mant1 - mant2
            result_sign = sign1
        else:
            result_mant = mant2 - mant1
            result_sign = sign2
    if result_mant == 0:
        return "0" * 32
    while result_mant >= (1 << 24):
        result_mant >>= 1
        exp += 1
    while result_mant < (1 << 23):
        result_mant <<= 1
        exp -= 1
    frac = result_mant - (1 << 23)
    exp_bits = ""
    temp_exp = exp
    for _ in range(8):
        exp_bits = ("1" if (temp_exp % 2) == 1 else "0") + exp_bits
        temp_exp //= 2
    frac_bits = ""
    for i in range(23):
        bit = (frac >> (22 - i)) & 1
        frac_bits += "1" if bit == 1 else "0"

    result_ieee = ("0" if result_sign == 0 else "1") + exp_bits + frac_bits
    return result_ieee


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
