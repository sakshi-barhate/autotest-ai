"""
parser.py
---------
Parses Python source code using the `ast` module to extract:
- Function names
- Parameters (and type hints, if present)
- Branches (if/else, loops, try/except)

This structured output is what gets passed to analyzer.py next,
NOT the raw source code — that separation is intentional.
"""

import ast


def parse_source(source_code: str) -> list[dict]:
    """
    Takes raw Python source code as a string and returns a list of
    dictionaries, one per function found, describing its structure.
    """
    tree = ast.parse(source_code)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(_parse_function(node))

    return functions


def _parse_function(node: ast.FunctionDef) -> dict:
    """Extracts structural details from a single function definition node."""
    params = []
    for arg in node.args.args:
        param_type = ast.unparse(arg.annotation) if arg.annotation else None
        params.append({"name": arg.arg, "type": param_type})

    branches = _find_branches(node)

    return {
        "name": node.name,
        "params": params,
        "branches": branches,
        "line_number": node.lineno,
    }


def _find_branches(node: ast.AST) -> list[dict]:
    """
    Walks through a function body and records each decision point:
    if/else, for/while loops, and try/except blocks.
    """
    branches = []

    for child in ast.walk(node):
        if isinstance(child, ast.If):
            branches.append({
                "type": "if",
                "condition": ast.unparse(child.test),
                "line_number": child.lineno,
            })
        elif isinstance(child, (ast.For, ast.While)):
            branches.append({
                "type": "loop",
                "line_number": child.lineno,
            })
        elif isinstance(child, ast.Try):
            branches.append({
                "type": "try_except",
                "line_number": child.lineno,
            })

    return branches


# Quick manual test — only runs if you execute this file directly
if __name__ == "__main__":
    sample_code = """
def calculate_discount(price: float, discount_percent: float) -> float:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount percentage")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return price - (price * discount_percent / 100)
"""
    result = parse_source(sample_code)
    import json
    print(json.dumps(result, indent=2))