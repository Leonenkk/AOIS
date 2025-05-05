import itertools

from .formula_analysis_tools import evaluate_ast, mark_subtrees, gather_subtrees, calculate_depth
from .formula_tree_generator import build_formula_tree


def compute_truth_table(logic_expression: str):
    syntax_tree = build_formula_tree(logic_expression)
    mark_subtrees(syntax_tree)
    all_components = gather_subtrees(syntax_tree)

    variable_components = [c for c in all_components if c.operation == 'variable']
    composite_components = [c for c in all_components if c.operation != 'variable']

    sorted_variables = sorted(variable_components, key=lambda x: x.variable)
    if syntax_tree.operation != 'variable':
        non_root_components = [c for c in composite_components if c is not syntax_tree]
        ordered_components = sorted(non_root_components, key=lambda x: calculate_depth(x))
        table_columns = sorted_variables + ordered_components + [syntax_tree]
    else:
        table_columns = sorted_variables

    header_labels = " | ".join(comp.formula for comp in table_columns)
    print(header_labels)
    print("-" * len(header_labels))

    sorted_variable_names = [v.variable for v in sorted_variables]
    variable_count = len(sorted_variable_names)
    truth_combinations = []
    binary_index = []

    for combination in itertools.product([0, 1], repeat=variable_count):
        context = {var: bool(val) for var, val in zip(sorted_variable_names, combination)}
        row_data = ["1" if evaluate_ast(node, context) else "0" for node in table_columns]
        func_value = 1 if evaluate_ast(syntax_tree, context) else 0

        truth_combinations.append((combination, func_value))
        binary_index.append("1" if func_value else "0")
        print(" | ".join(row_data))

    minimal_terms = []
    maximal_terms = []
    for bits, value in truth_combinations:
        term_index = int("".join(map(str, bits)), 2)
        minimal_terms.append(term_index) if value else maximal_terms.append(term_index)

    dnf_elements = [
        "(" + "∧".join(var if bit else "¬" + var for var, bit in zip(sorted_variable_names, bits)) + ")"
        for bits, value in truth_combinations if value
    ]

    cnf_elements = [
        "(" + "∨".join(var if not bit else "¬" + var for var, bit in zip(sorted_variable_names, bits)) + ")"
        for bits, value in truth_combinations if not value
    ]

    numeric_index = int("".join(binary_index), 2)
    padded_binary = format(numeric_index, f"0{2 ** variable_count}b")

    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ)")
    print(" ∨ ".join(dnf_elements))
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ)")
    print(" ∧ ".join(cnf_elements))
    print("\nЧисловые формы:")
    print(f"({', '.join(map(str, sorted(minimal_terms)))}) ∧")
    print(f"({', '.join(map(str, sorted(maximal_terms)))}) ∨")
    print("\nИндексная форма")
    print(f"{numeric_index} - {padded_binary}")

    return {
        'minimal_terms': sorted(minimal_terms),
        'maximal_terms': sorted(maximal_terms),
        'dnf_formula': " ∨ ".join(dnf_elements),
        'cnf_formula': " ∧ ".join(cnf_elements),
        'index_value': numeric_index,
        'binary_pattern': padded_binary,
        'variables': sorted_variable_names,
        'component_count': variable_count,
        'syntax_tree': syntax_tree
    }