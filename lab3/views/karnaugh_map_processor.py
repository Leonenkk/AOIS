def generate_gray_sequence(length: int) -> list:
    """Генерирует последовательность кодов Грея заданной длины"""
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer")
    return [num ^ (num >> 1) for num in range(1 << length)]


def _convert_to_binary_terms(input_terms: list, variable_count: int) -> list:
    """Конвертирует список терминов в бинарное представление"""
    if not isinstance(input_terms, list):
        raise TypeError("Input terms must be a list")
    if not isinstance(variable_count, int) or variable_count <= 0:
        raise ValueError("Variable count must be a positive integer")
    if any(not isinstance(term, int) or term < 0 for term in input_terms):
        raise ValueError("All terms must be non-negative integers")

    max_term = max(input_terms, default=0)
    if max_term >= (1 << variable_count):
        raise ValueError(f"Term {max_term} exceeds maximum value for {variable_count} variables")

    return [tuple((term >> i) & 1 for i in reversed(range(variable_count))) for term in input_terms]


def _combine_terms_pair(term_a: tuple, term_b: tuple) -> tuple:
    mismatch_count = 0
    combined = []
    for bit_a, bit_b in zip(term_a, term_b):
        combined.append(bit_a if bit_a == bit_b else '-')
        mismatch_count += (bit_a != bit_b)
    return tuple(combined) if mismatch_count == 1 else None


def _identify_prime_implicants(binary_terms: list, var_count: int) -> set:
    """Идентифицирует простые импликанты"""
    if not isinstance(binary_terms, list):
        raise TypeError("Binary terms must be a list")
    if not binary_terms:
        raise ValueError("Binary terms list cannot be empty")
    if not isinstance(var_count, int) or var_count <= 0:
        raise ValueError("Variable count must be a positive integer")

    grouped_terms = {}
    for term in binary_terms:
        if not isinstance(term, tuple) or len(term) != var_count:
            raise ValueError(f"Term {term} has invalid format or length")
        key = term.count(1)
        grouped_terms.setdefault(key, []).append(term)

    unchecked_terms = set(binary_terms)
    prime_set = set()

    while grouped_terms:
        next_group = {}
        processed = set()
        for key in sorted(grouped_terms):
            for t1 in grouped_terms[key]:
                for t2 in grouped_terms.get(key + 1, []):
                    merged = _combine_terms_pair(t1, t2)
                    if merged:
                        processed.update({t1, t2})
                        next_group.setdefault(merged.count(1), []).append(merged)

        prime_set.update(unchecked_terms - processed)
        unchecked_terms = set(sum(next_group.values(), []))
        grouped_terms = {k: v for k, v in next_group.items() if v}

    return prime_set


def _is_implicant_covering(implicant: tuple, minterm: tuple) -> bool:
    """Проверяет, покрывает ли импликант данный минтерм"""
    if not isinstance(implicant, tuple) or not isinstance(minterm, tuple):
        raise TypeError("Both arguments must be tuples")
    if len(implicant) != len(minterm):
        raise ValueError("Implicant and minterm must have equal length")

    return all(imp_bit == '-' or imp_bit == mt_bit for imp_bit, mt_bit in zip(implicant, minterm))


def _select_essential_implicants(prime_set: set, minterms: list) -> set:
    """Выбирает существенные импликанты"""
    if not isinstance(prime_set, set):
        raise TypeError("Prime set must be a set")
    if not isinstance(minterms, list):
        raise TypeError("Minterms must be a list")
    if not minterms:
        raise ValueError("Minterms list cannot be empty")

    coverage_table = {imp: [mt for mt in minterms if _is_implicant_covering(imp, mt)] for imp in prime_set}
    essential = set()
    covered = set()

    for mt in minterms:
        covering = [imp for imp in prime_set if _is_implicant_covering(imp, mt)]
        if not covering:
            raise ValueError(f"Minterm {mt} is not covered by any prime implicant")
        essential.add(covering[0]) if len(covering) == 1 else None

    for imp in essential:
        covered.update(coverage_table[imp])

    remaining = set(minterms) - covered
    while remaining:
        best = max(coverage_table.items(), key=lambda x: len(set(x[1]) & remaining))
        essential.add(best[0])
        remaining -= set(best[1])

    return essential


def optimize_kmap(input_terms: list, var_count: int, var_names: list, use_conjunctive: bool = True) -> list:
    """Оптимизирует карту Карно и возвращает упрощенное выражение"""
    if not isinstance(input_terms, list):
        raise TypeError("Input terms must be a list")
    if not isinstance(var_count, int) or var_count <= 0:
        raise ValueError("Variable count must be a positive integer")
    if not isinstance(var_names, list) or len(var_names) != var_count:
        raise ValueError("Variable names must be a list matching variable count")
    if any(not isinstance(name, str) for name in var_names):
        raise ValueError("All variable names must be strings")

    binary_terms = _convert_to_binary_terms(input_terms, var_count)
    primes = _identify_prime_implicants(binary_terms, var_count)
    essentials = _select_essential_implicants(primes, binary_terms)

    operator = '∧' if use_conjunctive else '∨'
    result = []
    for imp in essentials:
        components = []
        for var, bit in zip(var_names, imp):
            if bit == '-': continue
            components.append(
                var if (bit and use_conjunctive) else
                f"¬{var}" if (not bit and use_conjunctive) else
                f"¬{var}" if bit else var
            )
        result.append(f"({operator.join(components)})")

    return result


def display_kmap_table(terms: list, var_count: int, var_names: list, use_conjunctive: bool = True) -> None:
    """Отображает карту Карно в табличном формате"""
    if not isinstance(terms, list):
        raise TypeError("Terms must be a list")
    if not isinstance(var_count, int) or var_count <= 0:
        raise ValueError("Variable count must be a positive integer")
    if not isinstance(var_names, list) or len(var_names) != var_count:
        raise ValueError("Variable names must be a list matching variable count")
    if any(not isinstance(name, str) for name in var_names):
        raise ValueError("All variable names must be strings")

    row_bits = var_count // 2
    col_bits = var_count - row_bits
    row_codes = generate_gray_sequence(row_bits)
    col_codes = generate_gray_sequence(col_bits)
    term_set = set(terms)

    header_row = f"{''.join(var_names[:row_bits]):>{row_bits}} \\ {''.join(var_names[row_bits:]):<{col_bits}}"
    print(f"{header_row} | {' | '.join(f"{code:0{col_bits}b}" for code in col_codes)} |")
    print("-" * (len(header_row) + 4 + (col_bits + 3) * len(col_codes)))

    for rc in row_codes:
        row_str = f"{rc:0{row_bits}b}"
        print(f"{row_str:>{row_bits}}   |", end=" ")
        for cc in col_codes:
            full_code = (rc << col_bits) | cc
            cell_value = '1' if (use_conjunctive and full_code in term_set) or (
                    not use_conjunctive and full_code not in term_set) else '0'
            print(f" {cell_value} ", end="|")
        print()