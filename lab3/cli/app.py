from lab3.views.truth_table_analyzer import compute_truth_table
from lab3.views.qm_algorithm_handler import optimize_cnf, optimize_dnf
from lab3.views.tabular_optimizer import optimize_tabular_dnf as tabular_dnf, optimize_tabular_cnf as tabular_cnf
from lab3.views.karnaugh_map_processor import optimize_kmap, display_kmap_table

def main():
    expression = input("Введите логическое выражение:\n")
    print("\nТаблица истинности с подвыражениями:\n")

    # Получение данных таблицы истинности
    truth_data = compute_truth_table(expression)

    # Извлечение данных с новыми ключами
    min_terms = truth_data['minimal_terms']
    max_terms = truth_data['maximal_terms']
    var_count = truth_data['component_count']
    sorted_vars = truth_data['variables']

    print("\n========== Результаты минимизации ==========")

    # Минимизация СДНФ
    dnf_calculated = optimize_dnf(min_terms, var_count, sorted_vars)
    dnf_tabular = tabular_dnf(min_terms, var_count, sorted_vars)
    dnf_kmap = optimize_kmap(min_terms, var_count, sorted_vars, use_conjunctive=True)

    # Минимизация СКНФ
    cnf_calculated = optimize_cnf(max_terms, var_count, sorted_vars)
    cnf_tabular = tabular_cnf(max_terms, var_count, sorted_vars)
    cnf_kmap = optimize_kmap(max_terms, var_count, sorted_vars, use_conjunctive=False)

    # Вывод карт Карно
    print("\nКарта для DNF (1→единицы):")
    display_kmap_table(min_terms, var_count, sorted_vars, use_conjunctive=True)

    print("\nКарта для CNF (0→нули):")
    display_kmap_table(max_terms, var_count, sorted_vars, use_conjunctive=False)

    # Итоговый результат
    print("\n======= Итоговый результат =======")
    print("\nРезультаты минимизации для СДНФ:")
    print(f"  1) Расчетный метод: {dnf_calculated}")
    print(f"  2) Расчетно-табличный метод: {dnf_tabular}")
    print(f"  3) Метод Карно: {' ∨ '.join(dnf_kmap)}")

    print("\nРезультаты минимизации для СКНФ:")
    print(f"  1) Расчетный метод: {cnf_calculated}")
    print(f"  2) Расчетно-табличный метод: {cnf_tabular}")
    print(f"  3) Метод Карно: {' ∧ '.join(cnf_kmap)}")


if __name__ == "__main__":
    main()


#!a->(!(b|c))
#a&b&c&!d&!e
#a&b&c&d|e
