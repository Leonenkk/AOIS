from .node import Node,tokenize,preprocess_expression

def shunting_yard(tokens):
    precedence = {'!': 4, '&': 3, '|': 2, '->': 1, '~': 0}
    right_assoc = {'!': True, '&': False, '|': False, '->': False, '~': False}
    output_queue = []
    op_stack = []
    for token in tokens:
        if token.isalpha():
            output_queue.append(token)
        elif token == '!':
            op_stack.append(token)
        elif token in ['&','|','->','~']:
            while op_stack and op_stack[-1] != '(':
                top = op_stack[-1]
                if top not in precedence:
                    break
                top_prec = precedence[top]
                cur_prec = precedence[token]
                if right_assoc.get(token, False):
                    if top_prec > cur_prec:
                        output_queue.append(op_stack.pop())
                    else:
                        break
                else:
                    if top_prec >= cur_prec:
                        output_queue.append(op_stack.pop())
                    else:
                        break
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            if op_stack and op_stack[-1] == '(':
                op_stack.pop()
        else:
            raise ValueError(f"Неизвестный токен: {token}")
    while op_stack:
        output_queue.append(op_stack.pop())
    return output_queue

def rpn_to_ast(rpn_tokens):
    stack = []
    for token in rpn_tokens:
        if token.isalpha():
            stack.append(Node('var', var=token))
        elif token == '!':
            if not stack:
                raise ValueError("Ошибка: недостаточно операндов для '!'")
            operand = stack.pop()
            stack.append(Node('not', left=operand))
        elif token in ['&','|','->','~']:
            if len(stack) < 2:
                raise ValueError(f"Ошибка: недостаточно операндов для {token}")
            right = stack.pop()
            left = stack.pop()
            if token == '&':
                node_type = 'and'
            elif token == '|':
                node_type = 'or'
            elif token == '->':
                node_type = 'implies'
            elif token == '~':
                node_type = 'equiv'
            stack.append(Node(node_type, left=left, right=right))
        else:
            raise ValueError(f"Неизвестный токен в ОПЗ: {token}")
    if len(stack) != 1:
        raise ValueError("Ошибка: некорректное выражение (лишние операнды/операторы)")
    return stack[0]

def parse_expression(expr: str) -> Node:
    expr_prepared = preprocess_expression(expr)
    tokens = tokenize(expr_prepared)
    rpn = shunting_yard(tokens)
    ast = rpn_to_ast(rpn)
    return ast