def write_test_file(test_data: dict, source_function_name: str, output_dir: str = "generated_tests") -> str:
    import os
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"test_{source_function_name}.py")

    lines = []
    lines.append(f"from examples.sample_code import {source_function_name}")
    lines.append("import pytest")
    lines.append("")

    for case in test_data["test_cases"]:
        test_name = f"test_{case['name']}"
        inputs = case["inputs"]
        expected = case["expected_behavior"]
        case_type = case["type"]

        args_str = ", ".join(f"{k}={v}" for k, v in inputs.items())

        lines.append(f"def {test_name}():")
        lines.append(f"    \"\"\"{case_type}: {expected}\"\"\"")

        if case_type == "negative":
            lines.append(f"    with pytest.raises((ValueError, TypeError)):")
            lines.append(f"        {source_function_name}({args_str})")
        elif case_type == "load":
            lines.append(f"    for _ in range(10000):")
            lines.append(f"        {source_function_name}({args_str})")
        else:
            lines.append(f"    result = {source_function_name}({args_str})")
            lines.append(f"    assert result is not None")

        lines.append("")

    with open(file_path, "w") as f:
        f.write("\n".join(lines))

    return file_path


if __name__ == "__main__":
    from parser import parse_source
    from analyzer import analyze_functions
    from generator import generate_test_cases

    sample_code = """
def is_palindrome(text: str) -> bool:
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]
"""
    parsed = parse_source(sample_code)
    analyzed = analyze_functions(parsed)
    test_data = generate_test_cases(analyzed[0])

    output_path = write_test_file(test_data, "is_palindrome")
    print(f"Test file written to: {output_path}")