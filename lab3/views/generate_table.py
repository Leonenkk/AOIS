import itertools

from .label import evaluate_ast,label_sub_expressions,collect_sub_expressions_in_order,compute_depth
from .to_rpn import parse_expression

def generate_truth_table_and_forms(expr: str):
    ast = parse_expression(expr)
    label_sub_expressions(ast)
    all_nodes = collect_sub_expressions_in_order(ast)
    var_nodes = [n for n in all_nodes if n.node_type == 'var']
    complex_nodes = [n for n in all_nodes if n.node_type != 'var']
    var_nodes_sorted = sorted(var_nodes, key=lambda n: n.var)
    if ast.operation != 'var':
        non_root_complex = [n for n in complex_nodes if n is not ast]
        non_root_complex = sorted(non_root_complex, key=lambda n: compute_depth(n))
        columns = var_nodes_sorted + non_root_complex + [ast]
    else:
        columns = var_nodes_sorted
    header = " | ".join(node.formula for node in columns)
    print(header)
    print("-" * len(header))
    vars_sorted = [n.var for n in var_nodes_sorted]
    n_vars = len(vars_sorted)
    truth_rows = []
    index_bits = []
    for combo in itertools.product([0, 1], repeat=n_vars):
        env = {var: bool(val) for var, val in zip(vars_sorted, combo)}
        row_vals = []
        for node in columns:
            row_vals.append("1" if evaluate_ast(node, env) else "0")
        f_val = 1 if evaluate_ast(ast, env) else 0
        truth_rows.append((combo, f_val))
        index_bits.append("1" if f_val else "0")
        print(" | ".join(row_vals))
    minterms = []
    maxterms = []
    for combo, f_val in truth_rows:
        index = int("".join(str(bit) for bit in combo), 2)
        if f_val == 1:
            minterms.append(index)
        else:
            maxterms.append(index)
    dnf_terms = []
    cnf_terms = []
    for combo, f_val in truth_rows:
        if f_val == 1:
            term_literals = []
            for bit, var in zip(combo, vars_sorted):
                term_literals.append(var if bit == 1 else "¬" + var)
            dnf_terms.append("(" + "∧".join(term_literals) + ")")
        else:
            term_literals = []
            for bit, var in zip(combo, vars_sorted):
                term_literals.append(var if bit == 0 else "¬" + var)
            cnf_terms.append("(" + "∨".join(term_literals) + ")")
    dnf_formula = " ∨ ".join(dnf_terms)
    cnf_formula = " ∧ ".join(cnf_terms)
    binary_str = "".join(index_bits)
    index_value = int(binary_str, 2)
    binary_str_padded = format(index_value, f"0{2 ** n_vars}b")
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ)")
    print(dnf_formula)
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ)")
    print(cnf_formula)
    print("\nЧисловые формы:")
    print("(" + ", ".join(str(i) for i in sorted(minterms)) + ") ∧")
    print("(" + ", ".join(str(i) for i in sorted(maxterms)) + ") ∨")
    print("\nИндексная форма")
    print(f"{index_value} - {binary_str_padded}")
    return {
        'minterms': sorted(minterms),
        'maxterms': sorted(maxterms),
        'dnf_formula': dnf_formula,
        'cnf_formula': cnf_formula,
        'index_value': index_value,
        'binary_str_padded': binary_str_padded,
        'vars_sorted': vars_sorted,
        'n_vars': n_vars,
        'ast': ast
    }
