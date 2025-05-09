from .expression_nodes import ExpressionNode, clean_input, parse_symbols


def dijkstra_algorithm(symbol_list: list) -> list:
    """Преобразует список символов в обратную польскую нотацию (RPN)"""
    if not isinstance(symbol_list, list):
        raise TypeError("symbol_list must be a list")

    precedence = {'!': 4, '&': 3, '|': 2, '->': 1, '~': 0}
    associativity = {'!': 'right', '&': 'left', '|': 'left', '->': 'left', '~': 'left'}
    output = []
    stack = []

    for token in symbol_list:
        if not isinstance(token, str):
            raise TypeError(f"All tokens must be strings, got {type(token)}")

        if token.isalpha():
            if not token.islower():
                raise ValueError(f"Variables must be lowercase, got '{token}'")
            output.append(token)

        elif token == '!':
            stack.append(token)

        elif token in precedence:
            if token == '->' and len(token) != 2:
                raise ValueError("Implication operator must be '->'")

            while stack and stack[-1] != '(':
                prev = stack[-1]
                if (associativity[token] == 'left' and precedence[token] <= precedence.get(prev, 0)) or \
                        (associativity[token] == 'right' and precedence[token] < precedence.get(prev, 0)):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            if not stack:
                raise ValueError("Mismatched parentheses - closing parenthesis without opening")

            while stack and stack[-1] != '(':
                output.append(stack.pop())

            if not stack:
                raise ValueError("Mismatched parentheses - no opening parenthesis found")
            stack.pop()

        else:
            raise ValueError(f"Unknown token: '{token}'")

    while stack:
        if stack[-1] == '(':
            raise ValueError("Mismatched parentheses - unclosed opening parenthesis")
        output.append(stack.pop())

    return output


def convert_to_tree(rpn_elements: list) -> ExpressionNode:
    """Преобразует RPN-выражение в дерево выражений"""
    if not isinstance(rpn_elements, list):
        raise TypeError("rpn_elements must be a list")

    node_stack = []
    operation_map = {
        '&': 'conjunction',
        '|': 'disjunction',
        '->': 'implication',
        '~': 'equivalence'
    }

    for element in rpn_elements:
        if not isinstance(element, str):
            raise TypeError(f"All elements must be strings, got {type(element)}")

        if element.isalpha():
            if not element.islower():
                raise ValueError(f"Variables must be lowercase, got '{element}'")
            node_stack.append(ExpressionNode('variable', variable=element))

        elif element == '!':
            if not node_stack:
                raise ValueError("Not enough operands for negation")
            operand = node_stack.pop()
            node_stack.append(ExpressionNode('negation', lhs=operand))

        elif element in operation_map:
            if len(node_stack) < 2:
                raise ValueError(f"Not enough operands for operation '{element}'")
            rhs = node_stack.pop()
            lhs = node_stack.pop()
            node_stack.append(ExpressionNode(
                operation_map[element],
                lhs=lhs,
                rhs=rhs
            ))

        else:
            raise ValueError(f"Unknown element in RPN: '{element}'")

    if len(node_stack) != 1:
        raise ValueError("Invalid RPN expression - stack should contain exactly one element at the end")

    return node_stack[0]


def build_formula_tree(input_str: str) -> ExpressionNode:
    """Строит дерево формул из входной строки"""
    if not isinstance(input_str, str):
        raise TypeError("input_str must be a string")

    try:
        normalized = clean_input(input_str)
        tokens = parse_symbols(normalized)

        if not tokens:
            raise ValueError("Empty formula after parsing")

        rpn = dijkstra_algorithm(tokens)

        if not rpn:
            raise ValueError("Empty RPN expression generated")

        return convert_to_tree(rpn)
    except Exception as e:
        raise ValueError(f"Error building formula tree: {str(e)}") from e