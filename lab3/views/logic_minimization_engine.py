def convert_number_to_bits(value: int, bit_length: int) -> str:
    """Конвертирует число в битовую строку заданной длины"""
    if not isinstance(value, int) or value < 0:
        raise ValueError("Value must be a non-negative integer")
    if not isinstance(bit_length, int) or bit_length <= 0:
        raise ValueError("Bit length must be a positive integer")
    if value >= (1 << bit_length):
        raise ValueError(f"Value {value} cannot be represented with {bit_length} bits")

    return format(value, f'0{bit_length}b')


def merge_implicants(term_a: str, term_b: str) -> str:
    """Объединяет два импликанта если они отличаются на 1 бит"""
    if not isinstance(term_a, str) or not isinstance(term_b, str):
        raise TypeError("Both terms must be strings")
    if len(term_a) != len(term_b):
        raise ValueError("Terms must have equal length")
    if not all(c in ('0', '1', '-') for c in term_a):
        raise ValueError("Term A contains invalid characters")
    if not all(c in ('0', '1', '-') for c in term_b):
        raise ValueError("Term B contains invalid characters")

    difference_count = 0
    combined_result = []
    for bit_a, bit_b in zip(term_a, term_b):
        combined_result.append(bit_a if bit_a == bit_b else '-')
        difference_count += (bit_a != bit_b)
    return ''.join(combined_result) if difference_count == 1 else None


def translate_binary_to_literals(binary_pattern: str, variables: list, use_conjunction: bool) -> str:
    """Преобразует бинарный шаблон в литералы"""
    if not isinstance(binary_pattern, str):
        raise TypeError("Binary pattern must be a string")
    if not isinstance(variables, list):
        raise TypeError("Variables must be a list")
    if len(binary_pattern) != len(variables):
        raise ValueError("Binary pattern length must match variables count")
    if not all(c in ('0', '1', '-') for c in binary_pattern):
        raise ValueError("Binary pattern contains invalid characters")
    if not all(isinstance(var, str) for var in variables):
        raise ValueError("All variables must be strings")

    literals = []
    for bit, variable in zip(binary_pattern, variables):
        if bit == '-':
            continue
        prefix = '' if (bit == '1') ^ (not use_conjunction) else '¬'
        literals.append(f"{prefix}{variable}")
    operator = '∧' if use_conjunction else '∨'
    return operator.join(literals) or ('1' if use_conjunction else '0')


def extract_literals_from_pattern(binary_pattern: str, variables: list, is_conjunctive: bool) -> set:
    """Извлекает литералы из бинарного шаблона"""
    if not isinstance(binary_pattern, str):
        raise TypeError("Binary pattern must be a string")
    if not isinstance(variables, list):
        raise TypeError("Variables must be a list")
    if len(binary_pattern) != len(variables):
        raise ValueError("Binary pattern length must match variables count")
    if not all(c in ('0', '1', '-') for c in binary_pattern):
        raise ValueError("Binary pattern contains invalid characters")
    if not all(isinstance(var, str) for var in variables):
        raise ValueError("All variables must be strings")

    return {
        f"{'' if (bit == '1') ^ (not is_conjunctive) else '¬'}{var}"
        for bit, var in zip(binary_pattern, variables) if bit != '-'
    }


def is_implicant_covering_term(implicant: str, binary_term: str) -> bool:
    """Проверяет, покрывает ли импликант заданный терм"""
    if not isinstance(implicant, str) or not isinstance(binary_term, str):
        raise TypeError("Both arguments must be strings")
    if len(implicant) != len(binary_term):
        raise ValueError("Implicant and term must have equal length")
    if not all(c in ('0', '1', '-') for c in implicant):
        raise ValueError("Implicant contains invalid characters")
    if not all(c in ('0', '1') for c in binary_term):
        raise ValueError("Binary term contains invalid characters")

    return all(imp_bit == '-' or imp_bit == term_bit
               for imp_bit, term_bit in zip(implicant, binary_term))


def prune_redundant_implicants(prime_implicants: list, minterms: list, bit_count: int) -> list:
    """Удаляет избыточные импликанты"""
    if not isinstance(prime_implicants, list):
        raise TypeError("Prime implicants must be a list")
    if not isinstance(minterms, list):
        raise TypeError("Minterms must be a list")
    if not isinstance(bit_count, int) or bit_count <= 0:
        raise ValueError("Bit count must be a positive integer")
    if not prime_implicants:
        raise ValueError("Prime implicants list cannot be empty")
    if not minterms:
        raise ValueError("Minterms list cannot be empty")

    current_implicants = prime_implicants.copy()
    modified = True

    while modified:
        modified = False
        for current_implicant in current_implicants.copy():
            remaining_implicants = [imp for imp in current_implicants if imp != current_implicant]
            if all(any(is_implicant_covering_term(candidate, format(t, f'0{bit_count}b'))
                       for candidate in remaining_implicants) for t in minterms):
                current_implicants.remove(current_implicant)
                modified = True

    return current_implicants


def consolidate_implicants(prime_implicants: list, variables: list, is_conjunctive: bool) -> list:
    """Консолидирует импликанты, удаляя покрываемые"""
    if not isinstance(prime_implicants, list):
        raise TypeError("Prime implicants must be a list")
    if not isinstance(variables, list):
        raise TypeError("Variables must be a list")
    if not prime_implicants:
        raise ValueError("Prime implicants list cannot be empty")
    if len(prime_implicants[0]) != len(variables):
        raise ValueError("Implicant length must match variables count")

    literal_collection = [
        (imp, extract_literals_from_pattern(imp, variables, is_conjunctive))
        for imp in prime_implicants
    ]
    essential_implicants = []

    for idx, (current_imp, current_set) in enumerate(literal_collection):
        if not any(other_set.issubset(current_set)
                   for other_idx, (_, other_set) in enumerate(literal_collection)
                   if idx != other_idx):
            essential_implicants.append(current_imp)

    return essential_implicants