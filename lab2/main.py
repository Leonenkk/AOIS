def parse_expression(expr):
    """Парсинг логического выражения и извлечение переменных"""
    variables = sorted(set([c for c in expr if c in 'abcde']))
    expr = expr.replace(' ', '').replace('∨', '|').replace('∧', '&')
    expr = expr.replace('→', '>').replace('∼', '=').replace('¬', '!')
    return variables, expr


def evaluate_postfix(postfix, values):
    """Вычисление постфиксного выражения"""
    stack = []
    for token in postfix:
        if token == '!':
            a = stack.pop()
            stack.append(1 - a)
        elif token in '&|>=':
            b = stack.pop()
            a = stack.pop()
            if token == '&':
                stack.append(a & b)
            elif token == '|':
                stack.append(a | b)
            elif token == '>':
                stack.append(0 if a == 1 and b == 0 else 1)
            elif token == '=':
                stack.append(1 if a == b else 0)
        else:
            stack.append(values[token])
    return stack[0]


def shunting_yard(expr):
    """Алгоритм сортировочной станции для преобразования в постфиксную форму"""
    precedence = {'!': 4, '&': 3, '|': 2, '>': 1, '=': 1}
    output = []
    stack = []

    i = 0
    while i < len(expr):
        c = expr[i]
        if c in 'abcde':
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif c == '!':
            stack.append(c)
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(c, 0):
                output.append(stack.pop())
            stack.append(c)
        i += 1

    while stack:
        output.append(stack.pop())

    return output


def generate_truth_table(variables, postfix):
    """Генерация таблицы истинности"""
    n = len(variables)
    table = []
    for i in range(2 ** n):
        combo = [(i >> (n - 1 - j)) & 1 for j in range(n)]
        values = dict(zip(variables, combo))
        result = evaluate_postfix(postfix, values)
        table.append((combo, result))
    return table


def build_forms(table, variables):
    """Построение СДНФ, СКНФ и числовых форм"""
    sdnf = []
    sknf = []
    numeric_sdnf = []
    numeric_sknf = []
    index = 0

    for row, (combo, res) in enumerate(table):
        index = (index << 1) | res

        if res == 1:
            numeric_sdnf.append(str(row))
            terms = []
            for var, val in zip(variables, combo):
                terms.append(f"{'' if val else '¬'}{var}")
            sdnf.append('(' + ' ∧ '.join(terms) + ')')

        if res == 0:
            numeric_sknf.append(str(row))
            terms = []
            for var, val in zip(variables, combo):
                terms.append(f"{'¬' if val else ''}{var}")
            sknf.append('(' + ' ∨ '.join(terms) + ')')

    return {
        'sdnf': ' ∨ '.join(sdnf),
        'sknf': ' ∧ '.join(sknf),
        'numeric_sdnf': ', '.join(numeric_sdnf),
        'numeric_sknf': ', '.join(numeric_sknf),
        'index': f"{index} ({bin(index)[2:].zfill(len(table))})"
    }


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