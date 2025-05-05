
def gray_code(n):
    """Генерирует список Gray‑кодов длины n."""
    return [i ^ (i >> 1) for i in range(1 << n)]

def _to_binary_terms(terms, n_vars):
    return [tuple((t >> i) & 1 for i in reversed(range(n_vars))) for t in terms]

def _merge_pair(a, b):
    diff = 0
    merged = []
    for x, y in zip(a, b):
        if x != y:
            diff += 1
            merged.append('-')
        else:
            merged.append(x)
        if diff > 1:
            return None
    return tuple(merged) if diff == 1 else None

def _find_prime_implicants(terms, n_vars):
    groups = {}
    for t in terms:
        groups.setdefault(t.count(1), []).append(t)
    unchecked = set(terms)
    primes = set()
    while groups:
        new_groups = {}
        used = set()
        for i in sorted(groups):
            for t1 in groups[i]:
                for t2 in groups.get(i+1, []):
                    m = _merge_pair(t1, t2)
                    if m:
                        used |= {t1, t2}
                        new_groups.setdefault(m.count(1), []).append(m)
        primes |= (unchecked - used)
        unchecked = set(sum(new_groups.values(), []))
        groups = {}
        for t in unchecked:
            groups.setdefault(t.count(1), []).append(t)
    return primes

def _covers(pi, mt):
    return all(p == '-' or p == m for p, m in zip(pi, mt))

def _select_essential(primes, minterms):
    table = {pi: [mt for mt in minterms if _covers(pi, mt)] for pi in primes}
    essential = set()
    covered = set()
    for mt in minterms:
        cov = [pi for pi in primes if _covers(pi, mt)]
        if len(cov) == 1:
            essential.add(cov[0])
    for pi in essential:
        covered |= set(table[pi])
    rem = set(minterms) - covered
    while rem:
        pi, mts = max(table.items(), key=lambda kv: len(set(kv[1]) & rem))
        essential.add(pi)
        rem -= set(mts)
    return essential

def kmap_minimize(terms, n_vars, vars_, is_dnf=True):
    bits = _to_binary_terms(terms, n_vars)
    primes = _find_prime_implicants(bits, n_vars)
    essentials = _select_essential(primes, bits)
    sep = '∧' if is_dnf else '∨'
    out = []
    for pi in essentials:
        parts = []
        for name, b in zip(vars_, pi):
            if b == '-': continue
            if is_dnf:
                parts.append(name if b else f"¬{name}")
            else:
                parts.append(f"¬{name}" if b else name)
        out.append("(" + sep.join(parts) + ")")
    return out

def print_kmap_table(terms, n_vars, vars_, is_dnf=True):

    r = n_vars // 2
    c = n_vars - r
    row_codes = gray_code(r)
    col_codes = gray_code(c)
    term_set = set(terms)

    row_vars = "".join(vars_[:r])
    col_vars = "".join(vars_[r:])

    # Заголовок
    print(f"{row_vars:>{r}} \\ {col_vars:<{c}}", end=" | ")
    for code in col_codes:
        print(f"{code:0{c}b}", end=" | ")
    print()
    print("-" * ((c + 3) * (len(col_codes) + 1)))

    # Строки таблицы
    for rc in row_codes:
        row_bits = f"{rc:0{r}b}"
        print(f"{row_bits:>{r}}{' ' * (3 - r)}", end=" | ")
        for cc in col_codes:
            col_bits = f"{cc:0{c}b}"
            full = row_bits + col_bits
            idx = int(full, 2)
            val = 1 if is_dnf else 0
            cell = str(val) if idx in term_set else str(1 - val)
            print(f" {cell} ", end="|")
        print()

