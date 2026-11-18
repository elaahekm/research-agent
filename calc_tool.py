import ast
import operator

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("not allowed")


def calculate(expression):
    tree = ast.parse(expression, mode="eval")
    return _eval(tree.body)


if __name__ == "__main__":
    print(calculate("12 * (3 + 4)"))