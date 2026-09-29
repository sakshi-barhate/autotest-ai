from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.parser import parse_source
from app.analyzer import analyze_functions
from app.generator import generate_test_cases
from app.writer import write_test_file
from app.runner import run_coverage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeInput(BaseModel):
    source_code: str


@app.post("/analyze")
def analyze(input: CodeInput):
    try:
        parsed = parse_source(input.source_code)
        analyzed = analyze_functions(parsed)
        return {"functions": analyzed}
    except SyntaxError:
        return {"error": "The code you pasted has a syntax error. Please check it and try again."}
    except Exception:
        return {"error": "Something went wrong while analyzing the code."}


@app.post("/generate-tests")
def generate(input: CodeInput):
    try:
        parsed = parse_source(input.source_code)
        analyzed = analyze_functions(parsed)

        if not analyzed:
            return {"error": "No functions found in the provided code."}

        test_data = generate_test_cases(analyzed[0])
        function_name = analyzed[0]["name"]

        with open("examples/sample_code.py", "w") as f:
            f.write(input.source_code)

        file_path = write_test_file(test_data, function_name)

        return {"test_data": test_data, "file_path": file_path}
    except SyntaxError:
        return {"error": "The code you pasted has a syntax error. Please check it and try again."}
    except Exception:
        return {"error": "Something went wrong while generating tests."}


@app.post("/run-coverage")
def run(input: CodeInput):
    try:
        parsed = parse_source(input.source_code)
        analyzed = analyze_functions(parsed)

        if not analyzed:
            return {"error": "No functions found in the provided code."}

        function_name = analyzed[0]["name"]
        test_file_path = f"generated_tests/test_{function_name}.py"

        coverage_result = run_coverage(
            test_file_path=test_file_path,
            source_module="examples.sample_code"
        )
        return coverage_result
    except SyntaxError:
        return {"error": "The code you pasted has a syntax error. Please check it and try again."}
    except Exception:
        return {"error": "Something went wrong while measuring coverage."}