def convert_number_to_bits(value: int, bit_length: int) -> str:
    return format(value, f'0{bit_length}b')


def merge_implicants(term_a: str, term_b: str) -> str:
    difference_count = 0
    combined_result = []
    for bit_a, bit_b in zip(term_a, term_b):
        combined_result.append(bit_a if bit_a == bit_b else '-')
        difference_count += (bit_a != bit_b)
    return ''.join(combined_result) if difference_count == 1 else None


def translate_binary_to_literals(binary_pattern: str, variables: list, use_conjunction: bool) -> str:
    literals = []
    for bit, variable in zip(binary_pattern, variables):
        if bit == '-': continue
        prefix = '' if (bit == '1') ^ (not use_conjunction) else '¬'
        literals.append(f"{prefix}{variable}")
    operator = '∧' if use_conjunction else '∨'
    return operator.join(literals) or ('1' if use_conjunction else '0')


def extract_literals_from_pattern(binary_pattern: str, variables: list, is_conjunctive: bool) -> set:
    return {
        f"{'' if (bit == '1') ^ (not is_conjunctive) else '¬'}{var}"
        for bit, var in zip(binary_pattern, variables) if bit != '-'
    }


def is_implicant_covering_term(implicant: str, binary_term: str) -> bool:
    return all(imp_bit == '-' or imp_bit == term_bit
               for imp_bit, term_bit in zip(implicant, binary_term))


def prune_redundant_implicants(prime_implicants: list, minterms: list, bit_count: int) -> list:
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