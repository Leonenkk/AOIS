# formula_analysis_tools.py
from .expression_nodes import ExpressionNode


def mark_subtrees(root: ExpressionNode) -> None:
    """Рекурсивно аннотирует подформулы для всех узлов дерева"""
    if not isinstance(root, ExpressionNode):
        raise TypeError("Root must be an ExpressionNode")

    if root.operation == 'variable':
        if not hasattr(root, 'variable') or not isinstance(root.variable, str):
            raise ValueError("Variable node must have a string variable attribute")
        root.formula = root.variable

    elif root.operation == 'negation':
        if not hasattr(root, 'lhs') or root.lhs is None:
            raise ValueError("Negation node must have a left child")
        mark_subtrees(root.lhs)
        wrap = root.lhs.operation != 'variable'
        root.formula = f"¬({root.lhs.formula})" if wrap else f"¬{root.lhs.formula}"

    elif root.operation in {'conjunction', 'disjunction', 'implication', 'equivalence'}:
        if not hasattr(root, 'lhs') or root.lhs is None or not hasattr(root, 'rhs') or root.rhs is None:
            raise ValueError(f"Binary operation {root.operation} must have both left and right children")

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
    if not isinstance(node, ExpressionNode):
        raise TypeError("Node must be an ExpressionNode")

    if node.operation == 'variable':
        return 1
    if node.operation == 'negation':
        if not hasattr(node, 'lhs') or node.lhs is None:
            raise ValueError("Negation node must have a left child")
        return calculate_depth(node.lhs) + 1

    if not hasattr(node, 'lhs') or node.lhs is None or not hasattr(node, 'rhs') or node.rhs is None:
        raise ValueError(f"Binary operation {node.operation} must have both left and right children")
    return max(calculate_depth(node.lhs), calculate_depth(node.rhs)) + 1


def gather_subtrees(root: ExpressionNode) -> list:
    """Собирает все уникальные подформулы дерева"""
    if not isinstance(root, ExpressionNode):
        raise TypeError("Root must be an ExpressionNode")

    components = []
    visited = set()

    def traverse(node):
        if not node:
            return

        if not isinstance(node, ExpressionNode):
            raise TypeError("All nodes must be ExpressionNode instances")

        if node.operation in {'conjunction', 'disjunction', 'implication', 'equivalence'}:
            if not hasattr(node, 'lhs') or node.lhs is None or not hasattr(node, 'rhs') or node.rhs is None:
                raise ValueError(f"Binary operation {node.operation} must have both left and right children")
            traverse(node.lhs)
            if node.formula not in visited:
                visited.add(node.formula)
                components.append(node)
            traverse(node.rhs)

        elif node.operation == 'negation':
            if not hasattr(node, 'lhs') or node.lhs is None:
                raise ValueError("Negation node must have a left child")
            traverse(node.lhs)
            if node.formula not in visited:
                visited.add(node.formula)
                components.append(node)

        else:
            if node.operation != 'variable' or not hasattr(node, 'variable') or not isinstance(node.variable, str):
                raise ValueError("Invalid variable node")
            if node.formula not in visited:
                visited.add(node.formula)
                components.append(node)

    traverse(root)
    return components


def evaluate_ast(node: ExpressionNode, env: dict) -> bool:
    """Вычисляет значение формулы для заданных значений переменных"""
    if not isinstance(node, ExpressionNode):
        raise TypeError("Node must be an ExpressionNode")
    if not isinstance(env, dict):
        raise TypeError("Environment must be a dictionary")

    if node.operation == 'variable':
        if not hasattr(node, 'variable') or not isinstance(node.variable, str):
            raise ValueError("Variable node must have a string variable attribute")
        if node.variable not in env:
            raise ValueError(f"Variable {node.variable} not found in environment")
        return env[node.variable]

    if node.operation == 'negation':
        if not hasattr(node, 'lhs') or node.lhs is None:
            raise ValueError("Negation node must have a left child")
        return not evaluate_ast(node.lhs, env)

    if node.operation == 'conjunction':
        if not hasattr(node, 'lhs') or node.lhs is None or not hasattr(node, 'rhs') or node.rhs is None:
            raise ValueError("Conjunction must have both left and right children")
        return evaluate_ast(node.lhs, env) and evaluate_ast(node.rhs, env)

    if node.operation == 'disjunction':
        if not hasattr(node, 'lhs') or node.lhs is None or not hasattr(node, 'rhs') or node.rhs is None:
            raise ValueError("Disjunction must have both left and right children")
        return evaluate_ast(node.lhs, env) or evaluate_ast(node.rhs, env)

    if node.operation == 'implication':
        if not hasattr(node, 'lhs') or node.lhs is None or not hasattr(node, 'rhs') or node.rhs is None:
            raise ValueError("Implication must have both left and right children")
        return (not evaluate_ast(node.lhs, env)) or evaluate_ast(node.rhs, env)

    if node.operation == 'equivalence':
        if not hasattr(node, 'lhs') or node.lhs is None or not hasattr(node, 'rhs') or node.rhs is None:
            raise ValueError("Equivalence must have both left and right children")
        return evaluate_ast(node.lhs, env) == evaluate_ast(node.rhs, env)

    raise ValueError(f"Неизвестная операция: {node.operation}")