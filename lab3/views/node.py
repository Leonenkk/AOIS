class ExpressionNode:
    def __init__(self, operation, lhs=None, rhs=None, variable=None):
        self.operation = operation
        self.lhs = lhs
        self.rhs = rhs
        self.variable = variable
        self.formula = None

def clean_input(expression: str) -> str:
    return expression.replace(" ", "")

def parse_symbols(input_expr: str):
    symbol_list = []
    cursor = 0
    while cursor < len(input_expr):
        chunk = input_expr[cursor:cursor+2]
        symbol = "->" if chunk == "->" else None
        symbol = input_expr[cursor] if not symbol and input_expr[cursor] in {'(', ')', '!', '&', '|', '~'} else symbol
        symbol = input_expr[cursor] if not symbol and input_expr[cursor].isalpha() else symbol
        cursor += 2 if chunk == "->" else 1 if symbol else 1
        symbol_list.append(symbol) if symbol else None
    return symbol_list