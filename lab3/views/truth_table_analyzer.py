import itertools

from .formula_analysis_tools import evaluate_ast, mark_subtrees, gather_subtrees, calculate_depth
from .formula_tree_generator import build_formula_tree


def compute_truth_table(logic_expression: str) -> dict:
    """Вычисляет таблицу истинности для логического выражения"""
    # Валидация входных параметров
    if not isinstance(logic_expression, str):
        raise TypeError("Logic expression must be a string")
    if not logic_expression.strip():
        raise ValueError("Logic expression cannot be empty")

    # Построение синтаксического дерева
    try:
        syntax_tree = build_formula_tree(logic_expression)
    except Exception as e:
        raise ValueError(f"Error building syntax tree: {str(e)}") from e

    # Аннотация поддеревьев
    try:
        mark_subtrees(syntax_tree)
    except Exception as e:
        raise RuntimeError(f"Error marking subtrees: {str(e)}") from e

    # Сбор всех компонентов дерева
    try:
        all_components = gather_subtrees(syntax_tree)
    except Exception as e:
        raise RuntimeError(f"Error gathering subtrees: {str(e)}") from e

    if not all_components:
        raise RuntimeError("No components found in syntax tree")

    # Разделение на переменные и составные компоненты
    variable_components = [c for c in all_components if c.operation == 'variable']
    composite_components = [c for c in all_components if c.operation != 'variable']

    if not variable_components:
        raise RuntimeError("No variables found in the expression")

    # Сортировка переменных и компонентов
    sorted_variables = sorted(variable_components, key=lambda x: x.variable)
    sorted_variable_names = [v.variable for v in sorted_variables]
    variable_count = len(sorted_variable_names)

    # Подготовка столбцов таблицы
    if syntax_tree.operation != 'variable':
        non_root_components = [c for c in composite_components if c is not syntax_tree]
        try:
            ordered_components = sorted(non_root_components, key=lambda x: calculate_depth(x))
        except Exception as e:
            raise RuntimeError(f"Error calculating component depths: {str(e)}") from e
        table_columns = sorted_variables + ordered_components + [syntax_tree]
    else:
        table_columns = sorted_variables

    # Проверка формул перед выводом
    if any(not hasattr(c, 'formula') or c.formula is None for c in table_columns):
        raise RuntimeError("Some components are missing formula annotations")

    # Вывод заголовка таблицы
    header_labels = " | ".join(comp.formula for comp in table_columns)
    print(header_labels)
    print("-" * len(header_labels))

    # Генерация всех возможных комбинаций значений переменных
    truth_combinations = []
    binary_index = []

    for combination in itertools.product([0, 1], repeat=variable_count):
        context = {var: bool(val) for var, val in zip(sorted_variable_names, combination)}

        try:
            row_data = ["1" if evaluate_ast(node, context) else "0" for node in table_columns]
            func_value = 1 if evaluate_ast(syntax_tree, context) else 0
        except Exception as e:
            raise RuntimeError(f"Error evaluating expression for combination {combination}: {str(e)}") from e

        truth_combinations.append((combination, func_value))
        binary_index.append("1" if func_value else "0")
        print(" | ".join(row_data))

    # Подготовка минимальных и максимальных термов
    minimal_terms = []
    maximal_terms = []
    for bits, value in truth_combinations:
        term_index = int("".join(map(str, bits)), 2)
        minimal_terms.append(term_index) if value else maximal_terms.append(term_index)

    # Формирование СДНФ и СКНФ
    dnf_elements = [
        "(" + "∧".join(var if bit else "¬" + var for var, bit in zip(sorted_variable_names, bits)) + ")"
        for bits, value in truth_combinations if value
    ]

    cnf_elements = [
        "(" + "∨".join(var if not bit else "¬" + var for var, bit in zip(sorted_variable_names, bits)) + ")"
        for bits, value in truth_combinations if not value
    ]

    # Вычисление индексной формы
    try:
        numeric_index = int("".join(binary_index), 2)
        padded_binary = format(numeric_index, f"0{2 ** variable_count}b")
    except Exception as e:
        raise RuntimeError(f"Error calculating numeric index: {str(e)}") from e

    # Вывод результатов
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ)")
    print(" ∨ ".join(dnf_elements) if dnf_elements else "0")
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ)")
    print(" ∧ ".join(cnf_elements) if cnf_elements else "1")
    print("\nЧисловые формы:")
    print(f"({', '.join(map(str, sorted(minimal_terms)))}) ∧" if minimal_terms else "() ∧")
    print(f"({', '.join(map(str, sorted(maximal_terms)))}) ∨" if maximal_terms else "() ∨")
    print("\nИндексная форма")
    print(f"{numeric_index} - {padded_binary}")

    return {
        'minimal_terms': sorted(minimal_terms),
        'maximal_terms': sorted(maximal_terms),
        'dnf_formula': " ∨ ".join(dnf_elements) if dnf_elements else "0",
        'cnf_formula': " ∧ ".join(cnf_elements) if cnf_elements else "1",
        'index_value': numeric_index,
        'binary_pattern': padded_binary,
        'variables': sorted_variable_names,
        'component_count': variable_count,
        'syntax_tree': syntax_tree
    }