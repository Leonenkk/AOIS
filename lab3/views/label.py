from .node import Node


def label_sub_expressions(root: Node) -> None:
    if root.node_type == 'var':
        root.expr_str = root.var
    elif root.node_type == 'not':
        label_sub_expressions(root.left)
        if root.left.node_type in ('and','or','implies','equiv'):
            root.expr_str = f"¬({root.left.expr_str})"
        else:
            root.expr_str = f"¬{root.left.expr_str}"
    elif root.node_type == 'and':
        label_sub_expressions(root.left)
        label_sub_expressions(root.right)
        left_s = root.left.expr_str
        right_s = root.right.expr_str
        if root.left.node_type in ('or','implies','equiv'):
            left_s = f"({left_s})"
        if root.right.node_type in ('or','implies','equiv'):
            right_s = f"({right_s})"
        root.expr_str = f"{left_s}∧{right_s}"
    elif root.node_type == 'or':
        label_sub_expressions(root.left)
        label_sub_expressions(root.right)
        left_s = root.left.expr_str
        right_s = root.right.expr_str
        if root.left.node_type in ('implies','equiv'):
            left_s = f"({left_s})"
        if root.right.node_type in ('and','implies','equiv'):
            right_s = f"({right_s})"
        root.expr_str = f"{left_s}∨{right_s}"
    elif root.node_type == 'implies':
        label_sub_expressions(root.left)
        label_sub_expressions(root.right)
        left_s = root.left.expr_str
        if root.left.node_type in ('and','or','implies','equiv'):
            left_s = f"({left_s})"
        right_s = root.right.expr_str
        if root.right.node_type in ('and','or','implies','equiv'):
            right_s = f"({right_s})"
        root.expr_str = f"{left_s}→{right_s}"
    elif root.node_type == 'equiv':
        label_sub_expressions(root.left)
        label_sub_expressions(root.right)
        left_s = root.left.expr_str
        if root.left.node_type in ('and','or','implies','equiv'):
            left_s = f"({left_s})"
        right_s = root.right.expr_str
        if root.right.node_type in ('and','or','implies','equiv'):
            right_s = f"({right_s})"
        root.expr_str = f"{left_s}↔{right_s}"

def compute_depth(node: Node) -> int:
    if node.node_type == 'var':
        return 1
    elif node.node_type == 'not':
        return compute_depth(node.left) + 1
    else:
        return max(compute_depth(node.left), compute_depth(node.right)) + 1

def collect_sub_expressions_in_order(root: Node):
    visited = {}
    result = []
    def traverse(node):
        if not node:
            return
        if node.node_type in ('and','or','implies','equiv'):
            traverse(node.left)
            if node.expr_str not in visited:
                visited[node.expr_str] = node
                result.append(node)
            traverse(node.right)
        elif node.node_type == 'not':
            traverse(node.left)
            if node.expr_str not in visited:
                visited[node.expr_str] = node
                result.append(node)
        else:
            if node.expr_str not in visited:
                visited[node.expr_str] = node
                result.append(node)
    traverse(root)
    return result

def evaluate_ast(root: Node, env: dict) -> bool:
    if root.node_type == 'var':
        return env[root.var]
    elif root.node_type == 'not':
        return not evaluate_ast(root.left, env)
    elif root.node_type == 'and':
        return evaluate_ast(root.left, env) and evaluate_ast(root.right, env)
    elif root.node_type == 'or':
        return evaluate_ast(root.left, env) or evaluate_ast(root.right, env)
    elif root.node_type == 'implies':
        return (not evaluate_ast(root.left, env)) or evaluate_ast(root.right, env)
    elif root.node_type == 'equiv':
        return evaluate_ast(root.left, env) == evaluate_ast(root.right, env)
    else:
        raise ValueError("Неизвестный тип узла")

