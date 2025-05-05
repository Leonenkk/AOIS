def int_to_bin_str(num, n_vars):
    return format(num, '0{}b'.format(n_vars))

def combine_terms(t1, t2):
    diff = 0
    res = []
    for a, b in zip(t1, t2):
        if a == b:
            res.append(a)
        else:
            res.append('-')
            diff += 1
    return "".join(res) if diff == 1 else None

def bin_to_lits(bstr, vars_, is_dnf=True):
    res = []
    for ch, v in zip(bstr, vars_):
        if ch == '-':
            continue
        if is_dnf:
            res.append(v if ch == '1' else "¬" + v)
        else:
            res.append("¬" + v if ch == '1' else v)
    connector = "∧" if is_dnf else "∨"
    return connector.join(res) if res else ("1" if is_dnf else "0")

def literal_set_from_binary(bstr, vars_, is_dnf):
    lits = []
    for ch, v in zip(bstr, vars_):
        if ch == '-':
            continue
        if is_dnf:
            lits.append(v if ch == '1' else "¬" + v)
        else:
            lits.append("¬" + v if ch == '1' else v)
    return set(lits)

def covers(impl, bstr):
    return all(a == b or a == '-' for a, b in zip(impl, bstr))

def eliminate_redundant_implicants(implicants, terms, n_vars):
    reduced = list(implicants)
    changed = True
    while changed:
        changed = False
        for imp in list(reduced):
            test_set = [x for x in reduced if x != imp]
            all_covered = True
            for t in terms:
                b = int_to_bin_str(t, n_vars)
                if not any(covers(candidate, b) for candidate in test_set):
                    all_covered = False
                    break
            if all_covered:
                reduced.remove(imp)
                changed = True
    return reduced

def absorb_clauses(implicants, vars_, is_dnf):
    literal_sets = [(imp, literal_set_from_binary(imp, vars_, is_dnf)) for imp in implicants]
    result = []
    for i, (imp_i, set_i) in enumerate(literal_sets):
        redundant = False
        for j, (imp_j, set_j) in enumerate(literal_sets):
            if i != j and set_j <= set_i:
                redundant = True
                break
        if not redundant:
            result.append(imp_i)
    return result

