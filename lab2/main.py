from second_lab import *


def main():
    expr = input("Введите логическое выражение: ")
    variables, parsed_expr = parse_expression(expr)
    postfix = shunting_yard(parsed_expr)
    table = generate_truth_table(variables, postfix)
    forms = build_forms(table, variables)

    print("\nТаблица истинности:")
    header = ' | '.join(variables) + ' | Результат'
    print(header)
    print('-' * len(header))
    for combo, res in table:
        print(' | '.join(map(str, combo)) + f' | {res}')

    print("\nСДНФ:")
    print(forms['sdnf'])
    print("Числовая форма СДНФ: ∨(", forms['numeric_sdnf'], ")")

    print("\nСКНФ:")
    print(forms['sknf'])
    print("Числовая форма СКНФ: ∧(", forms['numeric_sknf'], ")")

    print("\nИндексная форма:")
    print(forms['index'])


if __name__ == "__main__":
    main()


#тестовые примеры для ввода
# ((a->b)&(b->c))->(a->c)
# ((a∨b)&(c->d))∼e
#a->(b->c)
#(a∨b)∧!c


