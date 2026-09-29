def analyze_functions(parsed_functions: list[dict]) -> list[dict]:
    for func in parsed_functions:
        func["suggested_edge_cases"] = _suggest_edge_cases(func)
    return parsed_functions


def _suggest_edge_cases(func: dict) -> list[dict]:
    edge_cases = []

    for param in func["params"]:
        param_name = param["name"]
        param_type = param["type"]

        type_based = _edge_cases_by_type(param_type)
        condition_based = _edge_cases_from_conditions(param_name, func["branches"])

        edge_cases.append({
            "param": param_name,
            "type": param_type,
            "suggested_values": type_based + condition_based,
        })

    return edge_cases


def _edge_cases_by_type(param_type: str) -> list[str]:
    if param_type in ("int", "float"):
        return ["0", "-1", "very large number", "None (missing value)"]
    elif param_type == "str":
        return ["'' (empty string)", "very long string", "None (missing value)"]
    elif param_type == "list":
        return ["[] (empty list)", "None (missing value)"]
    elif param_type == "bool":
        return ["True", "False"]
    else:
        return ["None (missing value)", "wrong type (e.g. string instead of expected type)"]


def _edge_cases_from_conditions(param_name: str, branches: list[dict]) -> list[str]:
    suggestions = []

    for branch in branches:
        condition = branch.get("condition", "")
        if param_name in condition:
            if "<" in condition or ">" in condition:
                suggestions.append(f"boundary value near condition: '{condition}'")

    return suggestions


if __name__ == "__main__":
    from parser import parse_source
    import json

    sample_code = """
def calculate_discount(price: float, discount_percent: float) -> float:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount percentage")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return price - (price * discount_percent / 100)
"""
    parsed = parse_source(sample_code)
    analyzed = analyze_functions(parsed)
    print(json.dumps(analyzed, indent=2))