from .qm_algorithm_handler import (
    identify_essential_implicants,
    prune_redundant_implicants,
    tabular_method_processor
)
from .logic_minimization_engine import (
    translate_binary_to_literals,
    consolidate_implicants
)


def optimize_tabular_dnf(terms, variable_count, variable_names):
    print("\n==== Минимизация СДНФ (расчётно-табличный метод) ====")
    prime_implicants = tabular_method_processor(terms, variable_count, variable_names, True)
    essential_set = identify_essential_implicants(prime_implicants, terms, variable_count, variable_names, True)
    optimized_set = prune_redundant_implicants(essential_set, terms, variable_count)

    result_terms = [f"({translate_binary_to_literals(imp, variable_names, True)})" for imp in optimized_set]
    minimized = " ∨ ".join(result_terms)
    print("\nРЕЗУЛЬТАТ (табличный метод, СДНФ): " + minimized)
    return minimized


def optimize_tabular_cnf(terms, variable_count, variable_names):
    print("\n==== Минимизация СКНФ (расчётно-табличный метод) ====")
    prime_implicants = tabular_method_processor(terms, variable_count, variable_names, False)
    essential_set = identify_essential_implicants(prime_implicants, terms, variable_count, variable_names, False)
    optimized_set = prune_redundant_implicants(essential_set, terms, variable_count)
    final_set = consolidate_implicants(optimized_set, variable_names, False)

    result_terms = [f"({translate_binary_to_literals(imp, variable_names, False)})" for imp in final_set]
    minimized = " ∧ ".join(result_terms)
    print("\nРЕЗУЛЬТАТ (табличный метод, СКНФ): " + minimized)
    return minimized


def display_kmap(grid_data, row_labels=None, col_labels=None):
    header = "         " + "  ".join(f"{label:12}" for label in col_labels) if col_labels else ""
    print(header)

    for idx, row in enumerate(grid_data):
        row_prefix = f"{row_labels[idx]:12} " if row_labels else ""
        print(row_prefix + "  ".join(f"{cell:12}" for cell in row))