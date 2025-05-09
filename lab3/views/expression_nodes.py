class ExpressionNode:
    def __init__(self, operation, lhs=None, rhs=None, variable=None):
        self.operation = operation
        self.lhs = lhs
        self.rhs = rhs
        self.variable = variable
        self.formula = None

def clean_input(expression: str) -> str:
    if not isinstance(expression, str):
        raise ValueError("Input expression must be a string")
    return expression.replace(" ", "")


def parse_symbols(input_expr: str) -> list:
    if not isinstance(input_expr, str):
        raise ValueError("Input expression must be a string")

    symbol_list = []
    cursor = 0
    input_len = len(input_expr)

    while cursor < input_len:
        # Проверка на выход за границы строки
        if cursor + 1 >= input_len:
            chunk = input_expr[cursor]
        else:
            chunk = input_expr[cursor:cursor + 2]

        symbol = None

        # Проверка на импликацию
        if chunk == "->":
            symbol = "->"
        # Проверка на операторы и скобки
        elif input_expr[cursor] in {'(', ')', '!', '&', '|', '~'}:
            symbol = input_expr[cursor]
        # Проверка на переменные
        elif input_expr[cursor].isalpha():
            symbol = input_expr[cursor]
        else:
            raise ValueError(f"Invalid symbol at position {cursor}: '{input_expr[cursor]}'")

        # Обновление курсора и добавление символа
        cursor += 2 if symbol == "->" else 1
        symbol_list.append(symbol)

    # Проверка на пустой ввод
    if not symbol_list:
        raise ValueError("Empty expression after parsing")

    return symbol_list