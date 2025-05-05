from .logic_minimization_engine import (
    convert_number_to_bits,
    translate_binary_to_literals,
    extract_literals_from_pattern,
    merge_implicants,
    prune_redundant_implicants,
    is_implicant_covering_term,
    consolidate_implicants
)


def compute_prime_implicants(input_terms, var_count, var_names, is_dnf=True):
    term_groups = {}
    for term in input_terms:
        bit_str = convert_number_to_bits(term, var_count)
        ones_count = bit_str.count('1')
        term_groups.setdefault(ones_count, set()).add(bit_str)

    print("\n=== Склеивание: Исходные группы ===")
    for key in sorted(term_groups):
        items = sorted(term_groups[key])
        print(f"Группа {key}: " + ", ".join(
            translate_binary_to_literals(x, var_names, is_dnf) for x in items))

    stage_num = 1
    final_implicants = []
    while True:
        new_groups = {}
        processed_terms = set()
        sorted_keys = sorted(term_groups.keys())

        for i in range(len(sorted_keys) - 1):
            for t1 in term_groups[sorted_keys[i]]:
                for t2 in term_groups[sorted_keys[i + 1]]:
                    merged = merge_implicants(t1, t2)
                    new_groups.setdefault(merged.count('1'), set()).add(merged) if merged else None
                    processed_terms.update({t1, t2}) if merged else None

        final_implicants.extend(t for k in term_groups for t in term_groups[k] if t not in processed_terms)

        if not new_groups:
            print(f"\n=== Склеивание завершено на стадии {stage_num} ===")
            break

        print(f"\n=== Стадия {stage_num} ===")
        for k in sorted(new_groups.keys()):
            items = sorted(new_groups[k])
            print(f"Группа {k}: " + ", ".join(
                translate_binary_to_literals(x, var_names, is_dnf) for x in items))

        stage_num += 1
        term_groups = new_groups

    return sorted(set(final_implicants))


def identify_essential_implicants(prime_set, terms, var_count, var_names, is_dnf=True):
    return prime_set if is_dnf else [
        imp for imp in prime_set if not any(
            extract_literals_from_pattern(imp, var_names, is_dnf).issubset(
                extract_literals_from_pattern(other, var_names, is_dnf)
            ) for other in prime_set if imp != other
        )
    ]


def optimize_dnf(minterms, var_count, var_names):
    print("\n==== Минимизация СДНФ (расчётный метод) ====")
    prime_set = compute_prime_implicants(minterms, var_count, var_names, True)
    essential_set = identify_essential_implicants(prime_set, minterms, var_count, var_names, True)
    optimized_set = prune_redundant_implicants(essential_set, minterms, var_count)

    result = " ∨ ".join(f"({translate_binary_to_literals(x, var_names, True)})" for x in optimized_set)
    result = " ∨ ".join(var_names) if result.strip() == "1" else result
    print("\nРЕЗУЛЬТАТ (расчётный метод, СДНФ): " + result)
    return result


def optimize_cnf(maxterms, var_count, var_names):
    print("\n==== Минимизация СКНФ (расчётный метод) ====")
    prime_set = compute_prime_implicants(maxterms, var_count, var_names, False)
    essential_set = identify_essential_implicants(prime_set, maxterms, var_count, var_names, False)
    optimized_set = prune_redundant_implicants(essential_set, maxterms, var_count)
    final_set = consolidate_implicants(optimized_set, var_names, False)

    result = " ∧ ".join(f"({translate_binary_to_literals(x, var_names, False)})" for x in final_set)
    print("\nРЕЗУЛЬТАТ (расчётный метод, СКНФ): " + result)
    return result


def construct_coverage_table(prime_set, terms, var_count, var_names, is_dnf=True):
    return {
        imp: ["Х" if is_implicant_covering_term(imp, convert_number_to_bits(t, var_count)) else "."
              for t in terms]
        for imp in prime_set
    }


def display_coverage_table(table_data, terms, var_names, is_dnf=True):
    header = [convert_term_to_clause(t, var_names, not is_dnf).replace(" ", ".") for t in terms]
    print("\nТаблица покрытия:\n" + " " * 20 + " ".join(f"{cell:16}" for cell in header))
    print("-" * (20 + 17 * len(header)))

    for imp in sorted(table_data.keys(), key=lambda x: x.count('-')):
        label = translate_binary_to_literals(imp, var_names, is_dnf)
        row = [cell if cell == "Х" else "." for cell in table_data[imp]]
        print(f"{label:20} | " + " ".join(f"{cell:16}" for cell in row))

def convert_term_to_clause(index, var_names, for_cnf=True):
    bits = format(index, f'0{len(var_names)}b')
    literals = [
        ("¬" + v if bit == '1' else v) if for_cnf
        else (v if bit == '1' else "¬" + v)
        for bit, v in zip(bits, var_names)
    ]
    return f"({('∨' if for_cnf else '∧').join(literals)})"

def tabular_method_processor(terms, var_count, var_names, is_dnf=True):
    prime_set = compute_prime_implicants(terms, var_count, var_names, is_dnf)
    coverage_table = construct_coverage_table(prime_set, terms, var_count, var_names, is_dnf)
    display_coverage_table(coverage_table, terms, var_names, is_dnf)
    return prime_set