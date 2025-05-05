# formula_analysis_tools.py
from .expression_nodes import ExpressionNode


def mark_subtrees(root: ExpressionNode) -> None:
    """Рекурсивно аннотирует подформулы для всех узлов дерева"""
    if root.operation == 'variable':
        root.formula = root.variable

    elif root.operation == 'negation':
        mark_subtrees(root.lhs)
        wrap = root.lhs.operation != 'variable'
        root.formula = f"¬({root.lhs.formula})" if wrap else f"¬{root.lhs.formula}"

    elif root.operation in {'conjunction', 'disjunction', 'implication', 'equivalence'}:
        mark_subtrees(root.lhs)
        mark_subtrees(root.rhs)

        # Определение необходимости скобок для левой части
        lhs_needs_wrap = root.lhs.operation in {
            'disjunction' if root.operation == 'conjunction' else 'implication',
            'equivalence'
        }

        # Определение необходимости скобок для правой части
        rhs_needs_wrap = root.rhs.operation in {
            'disjunction' if root.operation == 'conjunction' else 'implication',
            'equivalence'
        }

        # Формирование строкового представления
        operators = {
            'conjunction': '∧',
            'disjunction': '∨',
            'implication': '→',
            'equivalence': '↔'
        }

        lhs = f"({root.lhs.formula})" if lhs_needs_wrap else root.lhs.formula
        rhs = f"({root.rhs.formula})" if rhs_needs_wrap else root.rhs.formula
        root.formula = f"{lhs}{operators[root.operation]}{rhs}"

    else:
        raise ValueError(f"Неподдерживаемая операция: {root.operation}")


def calculate_depth(node: ExpressionNode) -> int:
    """Вычисляет глубину поддерева"""
    if node.operation == 'variable':
        return 1
    if node.operation == 'negation':
        return calculate_depth(node.lhs) + 1
    return max(calculate_depth(node.lhs), calculate_depth(node.rhs)) + 1


def gather_subtrees(root: ExpressionNode) -> list:
    """Собирает все уникальные подформулы дерева"""
    components = []
    visited = set()

    def traverse(node):
        if not node:
            return

        if node.operation in {'conjunction', 'disjunction', 'implication', 'equivalence'}:
            traverse(node.lhs)
            if node.formula not in visited:
                visited.add(node.formula)
                components.append(node)
            traverse(node.rhs)

        elif node.operation == 'negation':
            traverse(node.lhs)
            if node.formula not in visited:
                visited.add(node.formula)
                components.append(node)

        else:
            if node.formula not in visited:
                visited.add(node.formula)
                components.append(node)

    traverse(root)
    return components


def evaluate_ast(node: ExpressionNode, env: dict) -> bool:
    """Вычисляет значение формулы для заданных значений переменных"""
    if node.operation == 'variable':
        return env[node.variable]

    if node.operation == 'negation':
        return not evaluate_ast(node.lhs, env)

    if node.operation == 'conjunction':
        return evaluate_ast(node.lhs, env) and evaluate_ast(node.rhs, env)

    if node.operation == 'disjunction':
        return evaluate_ast(node.lhs, env) or evaluate_ast(node.rhs, env)

    if node.operation == 'implication':
        return (not evaluate_ast(node.lhs, env)) or evaluate_ast(node.rhs, env)

    if node.operation == 'equivalence':
        return evaluate_ast(node.lhs, env) == evaluate_ast(node.rhs, env)

    raise ValueError(f"Неизвестная операция: {node.operation}")