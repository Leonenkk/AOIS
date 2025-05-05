from .translate import int_to_bin_str,bin_to_lits,literal_set_from_binary,combine_terms,\
    eliminate_redundant_implicants,absorb_clauses,covers

def quine_mccluskey_calc(terms, n_vars, vars_, is_dnf=True):
    groups = {}
    for t in terms:
        b = int_to_bin_str(t, n_vars)
        ones = b.count('1')
        groups.setdefault(ones, set()).add(b)
    print("\n=== Склеивание: Исходные группы ===")
    for k in sorted(groups.keys()):
        items = sorted(groups[k])
        print(f"Группа {k}: " + ", ".join(bin_to_lits(x, vars_, is_dnf) for x in items))
    stage = 1
    final_combs = []
    while True:
        new_groups = {}
        combined_this_stage = set()
        sorted_keys = sorted(groups.keys())
        for i in range(len(sorted_keys) - 1):
            for term1 in groups[sorted_keys[i]]:
                for term2 in groups[sorted_keys[i+1]]:
                    comb = combine_terms(term1, term2)
                    if comb:
                        new_groups.setdefault(comb.count('1'), set()).add(comb)
                        combined_this_stage.add(term1)
                        combined_this_stage.add(term2)
        for k2 in groups:
            for t2 in groups[k2]:
                if t2 not in combined_this_stage:
                    final_combs.append(t2)
        if not new_groups:
            print(f"\n=== Склеивание завершено на стадии {stage} ===")
            break
        print(f"\n=== Стадия {stage} ===")
        for k3 in sorted(new_groups.keys()):
            items = sorted(new_groups[k3])
            print(f"Группа {k3}: " + ", ".join(bin_to_lits(x, vars_, is_dnf) for x in items))
        stage += 1
        groups = new_groups
    return sorted(set(final_combs))

def select_essential_calc(prime_implicants, terms, n_vars, vars_, is_dnf=True):
    if is_dnf:
        return prime_implicants
    else:
        remaining = list(prime_implicants)
        to_remove = set()
        for i in range(len(remaining)):
            for j in range(len(remaining)):
                if i != j:
                    set_i = literal_set_from_binary(remaining[i], vars_, is_dnf)
                    set_j = literal_set_from_binary(remaining[j], vars_, is_dnf)
                    if set_i <= set_j:
                        to_remove.add(remaining[j])
        return [imp for imp in remaining if imp not in to_remove]

#minimize

def minimize_calc_dnf(minterms, n_vars, vars_):
    print("\n==== Минимизация СДНФ (расчётный метод) ====")
    prime = quine_mccluskey_calc(minterms, n_vars, vars_, is_dnf=True)
    need = select_essential_calc(prime, minterms, n_vars, vars_, is_dnf=True)
    need = eliminate_redundant_implicants(need, minterms, n_vars)
    result_terms = []
    for x in need:
        result_terms.append("(" + bin_to_lits(x, vars_, True) + ")")
    minimized = " ∨ ".join(result_terms)
    if minimized.strip() == "1":
        minimized = " ∨ ".join(vars_)
    print("\nРЕЗУЛЬТАТ (расчётный метод, СДНФ): " + minimized)
    return minimized

def minimize_calc_cnf(maxterms, n_vars, vars_):
    print("\n==== Минимизация СКНФ (расчётный метод) ====")
    prime = quine_mccluskey_calc(maxterms, n_vars, vars_, is_dnf=False)
    need = select_essential_calc(prime, maxterms, n_vars, vars_, is_dnf=False)
    need = eliminate_redundant_implicants(need, maxterms, n_vars)
    need = absorb_clauses(need, vars_, is_dnf=False)
    result_terms = []
    for x in need:
        result_terms.append("(" + bin_to_lits(x, vars_, False) + ")")
    minimized = " ∧ ".join(result_terms)
    print("\nРЕЗУЛЬТАТ (расчётный метод, СКНФ): " + minimized)
    return minimized

def build_table(prime, terms, n_vars, vars_, is_dnf=True):
    table = {}
    for p in prime:
        row = []
        for t in terms:
            b = int_to_bin_str(t, n_vars)
            row.append("Х" if covers(p, b) else ".")
        table[p] = row
    return table



def print_table_coverage(table, terms, vars_, is_dnf=True):
    header_cells = [term_to_clause(t, vars_, for_cnf=(not is_dnf)) for t in terms]
    header_cells = [cell.replace(" ", ".") for cell in header_cells]
    header = " " * 20 + " ".join(f"{cell:16}" for cell in header_cells)
    print("\nТаблица покрытия:")
    print(header)
    print("-" * len(header))
    for p in sorted(table.keys()):
        row_label = bin_to_lits(p, vars_, is_dnf)
        row = [cell if cell == "Х" else "." for cell in table[p]]
        print(f"{row_label:20} | " + " ".join(f"{cell:16}" for cell in row))

def term_to_clause(index, var_names, for_cnf=True):
    n = len(var_names)
    bits = format(index, f'0{n}b')
    literals = []
    for bit, v in zip(bits, var_names):
        if for_cnf:
            literal = ("¬" + v) if bit == '1' else v
        else:
            literal = v if bit == '1' else ("¬" + v)
        literals.append(literal)
    if for_cnf:
        return "(" + "∨".join(literals) + ")"
    else:
        return "(" + "∧".join(literals) + ")"

def quine_mccluskey_tabular(terms, n_vars, vars_, is_dnf=True):
    prime = quine_mccluskey_calc(terms, n_vars, vars_, is_dnf=is_dnf)
    coverage = build_table(prime, terms, n_vars, vars_, is_dnf=is_dnf)
    print_table_coverage(coverage, terms, vars_, is_dnf=is_dnf)
    return prime
