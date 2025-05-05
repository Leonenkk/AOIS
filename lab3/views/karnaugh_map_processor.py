def generate_gray_sequence(length: int) -> list:
    return [num ^ (num >> 1) for num in range(1 << length)]


def _convert_to_binary_terms(input_terms: list, variable_count: int) -> list:
    return [tuple((term >> i) & 1 for i in reversed(range(variable_count))) for term in input_terms]


def _combine_terms_pair(term_a: tuple, term_b: tuple) -> tuple:
    mismatch_count = 0
    combined = []
    for bit_a, bit_b in zip(term_a, term_b):
        combined.append(bit_a if bit_a == bit_b else '-')
        mismatch_count += (bit_a != bit_b)
    return tuple(combined) if mismatch_count == 1 else None


def _identify_prime_implicants(binary_terms: list, var_count: int) -> set:
    grouped_terms = {}
    for term in binary_terms:
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
    return all(imp_bit == '-' or imp_bit == mt_bit for imp_bit, mt_bit in zip(implicant, minterm))


def _select_essential_implicants(prime_set: set, minterms: list) -> set:
    coverage_table = {imp: [mt for mt in minterms if _is_implicant_covering(imp, mt)] for imp in prime_set}
    essential = set()
    covered = set()

    for mt in minterms:
        covering = [imp for imp in prime_set if _is_implicant_covering(imp, mt)]
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