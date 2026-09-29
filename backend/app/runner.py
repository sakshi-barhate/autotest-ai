import subprocess
import json


def run_coverage(test_file_path: str, source_module: str) -> dict:
    subprocess.run(
        ["coverage", "run", "--source", source_module, "-m", "pytest", test_file_path],
        capture_output=True,
        text=True
    )

    result = subprocess.run(
        ["coverage", "json", "-o", "-"],
        capture_output=True,
        text=True
    )

    try:
        data = json.loads(result.stdout)
        totals = data["totals"]
        return {
            "percent_covered": totals["percent_covered"],
            "lines_covered": totals["covered_lines"],
            "lines_missing": totals["missing_lines"],
            "num_statements": totals["num_statements"],
        }
    except (json.JSONDecodeError, KeyError):
        return {"error": "Failed to measure coverage. Please try again."}


if __name__ == "__main__":
    coverage_result = run_coverage(
        test_file_path="generated_tests/test_is_palindrome.py",
        source_module="examples.sample_code"
    )
    print(json.dumps(coverage_result, indent=2))