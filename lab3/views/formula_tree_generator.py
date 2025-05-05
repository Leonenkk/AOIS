from .expression_nodes import ExpressionNode, clean_input, parse_symbols


def dijkstra_algorithm(symbol_list):
    precedence = {'!': 4, '&': 3, '|': 2, '->': 1, '~': 0}
    associativity = {'!': 'right', '&': 'left', '|': 'left', '->': 'left', '~': 'left'}
    output = []
    stack = []

    for token in symbol_list:
        if token.isalpha():
            output.append(token)

        elif token == '!':
            stack.append(token)

        elif token in precedence:
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
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output


def convert_to_tree(rpn_elements):
    node_stack = []
    operation_map = {
        '&': 'conjunction',
        '|': 'disjunction',
        '->': 'implication',
        '~': 'equivalence'
    }

    for element in rpn_elements:
        if element.isalpha():
            node_stack.append(ExpressionNode('variable', variable=element))

        elif element == '!':
            operand = node_stack.pop()
            node_stack.append(ExpressionNode('negation', lhs=operand))

        elif element in operation_map:
            rhs = node_stack.pop()
            lhs = node_stack.pop()
            node_stack.append(ExpressionNode(
                operation_map[element],
                lhs=lhs,
                rhs=rhs
            ))

    return node_stack[0]


def build_formula_tree(input_str: str) -> ExpressionNode:
    normalized = clean_input(input_str)
    tokens = parse_symbols(normalized)
    rpn = dijkstra_algorithm(tokens)
    return convert_to_tree(rpn)