import os
import json
from dotenv import load_dotenv

load_dotenv()


def generate_test_cases(analyzed_function: dict) -> dict:
    func_name = analyzed_function["name"]
    params = analyzed_function["params"]
    edge_case_data = analyzed_function.get("suggested_edge_cases", [])

    test_cases = []

    happy_inputs = _build_happy_path_inputs(params)
    test_cases.append({
        "name": "happy_path_normal_input",
        "type": "happy_path",
        "inputs": happy_inputs,
        "expected_behavior": "Function executes successfully with typical input"
    })

    for edge_group in edge_case_data:
        param_name = edge_group["param"]
        for value in edge_group["suggested_values"][:2]:
            test_inputs = dict(happy_inputs)
            test_inputs[param_name] = _clean_value_for_code(value, edge_group["type"])

            is_negative = "None" in value or "wrong type" in value
            test_cases.append({
                "name": f"edge_case_{param_name}_{len(test_cases)}",
                "type": "negative" if is_negative else "edge_case",
                "inputs": test_inputs,
                "expected_behavior": f"Tests behavior when {param_name} is {value}"
            })

    test_cases.append({
        "name": "load_repeated_calls",
        "type": "load",
        "inputs": happy_inputs,
        "expected_behavior": "Function handles 10,000 rapid sequential calls without error"
    })

    return {"function_name": func_name, "test_cases": test_cases}


def _build_happy_path_inputs(params: list[dict]) -> dict:
    inputs = {}
    for param in params:
        param_type = param["type"]
        if param_type in ("int", "float"):
            inputs[param["name"]] = 10
        elif param_type == "str":
            inputs[param["name"]] = "'hello'"
        elif param_type == "bool":
            inputs[param["name"]] = "True"
        elif param_type == "list":
            inputs[param["name"]] = "[1, 2, 3]"
        else:
            inputs[param["name"]] = "'sample'"
    return inputs


def _clean_value_for_code(value: str, param_type: str) -> str:
    if "0" == value:
        return "0"
    if "-1" == value:
        return "-1"
    if "empty string" in value:
        return "''"
    if "empty list" in value:
        return "[]"
    if "True" == value:
        return "True"
    if "False" == value:
        return "False"
    if "very large number" in value:
        return "999999999"
    if "very long string" in value:
        return "'a' * 1000"
    if "None" in value:
        return "None"
    return "'test'"


if __name__ == "__main__":
    from parser import parse_source
    from analyzer import analyze_functions

    sample_code = """
def is_palindrome(text: str) -> bool:
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]
"""
    parsed = parse_source(sample_code)
    analyzed = analyze_functions(parsed)
    result = generate_test_cases(analyzed[0])
    print(json.dumps(result, indent=2))