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
    """Оптимизирует ДНФ табличным методом"""
    # Валидация входных параметров
    if not isinstance(terms, (list, set)):
        raise TypeError("Terms must be a list or set")
    if not terms:
        raise ValueError("Terms list cannot be empty")
    if not isinstance(variable_count, int) or variable_count <= 0:
        raise ValueError("Variable count must be a positive integer")
    if not isinstance(variable_names, list) or len(variable_names) != variable_count:
        raise ValueError("Variable names must be a list matching variable count")
    if any(not isinstance(name, str) for name in variable_names):
        raise ValueError("All variable names must be strings")

    print("\n==== Минимизация СДНФ (расчётно-табличный метод) ====")
    prime_implicants = tabular_method_processor(terms, variable_count, variable_names, True)
    essential_set = identify_essential_implicants(prime_implicants, terms, variable_count, variable_names, True)
    optimized_set = prune_redundant_implicants(essential_set, terms, variable_count)

    result_terms = [f"({translate_binary_to_literals(imp, variable_names, True)})" for imp in optimized_set]
    minimized = " ∨ ".join(result_terms)
    print("\nРЕЗУЛЬТАТ (табличный метод, СДНФ): " + minimized)
    return minimized


def optimize_tabular_cnf(terms, variable_count, variable_names):
    """Оптимизирует КНФ табличным методом"""
    # Валидация входных параметров
    if not isinstance(terms, (list, set)):
        raise TypeError("Terms must be a list or set")
    if not terms:
        raise ValueError("Terms list cannot be empty")
    if not isinstance(variable_count, int) or variable_count <= 0:
        raise ValueError("Variable count must be a positive integer")
    if not isinstance(variable_names, list) or len(variable_names) != variable_count:
        raise ValueError("Variable names must be a list matching variable count")
    if any(not isinstance(name, str) for name in variable_names):
        raise ValueError("All variable names must be strings")

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
    """Отображает карту Карно"""
    # Валидация входных параметров
    if not isinstance(grid_data, (list, tuple)):
        raise TypeError("Grid data must be a list or tuple")
    if not grid_data:
        raise ValueError("Grid data cannot be empty")

    if row_labels is not None:
        if not isinstance(row_labels, (list, tuple)):
            raise TypeError("Row labels must be a list or tuple")
        if len(row_labels) != len(grid_data):
            raise ValueError("Row labels count must match grid row count")

    if col_labels is not None:
        if not isinstance(col_labels, (list, tuple)):
            raise TypeError("Column labels must be a list or tuple")
        if len(col_labels) != len(grid_data[0]):
            raise ValueError("Column labels count must match grid column count")

    header = "         " + "  ".join(f"{label:12}" for label in col_labels) if col_labels else ""
    print(header)

    for idx, row in enumerate(grid_data):
        if not isinstance(row, (list, tuple)):
            raise TypeError(f"Row {idx} must be a list or tuple")
        row_prefix = f"{row_labels[idx]:12} " if row_labels else ""
        print(row_prefix + "  ".join(f"{cell:12}" for cell in row))