🔗 **Live demo:** https://autotest-ai-pi.vercel.app

AutoTest AI 🧪

An AI-assisted tool that analyzes Python functions and automatically generates edge-case, negative, and load test suites — then measures the real coverage improvement.

The Problem :
Developers usually only test the "happy path" — the normal, expected use of their code. Edge cases (empty inputs, negative numbers, None values, boundary conditions) are the most common source of production bugs, and writing tests for them is tedious and often skipped.

What It Does :
Parses Python code using AST (Abstract Syntax Tree) analysis to understand its structure — parameters, types, and decision branches (if/else, loops, try/except)
Analyzes that structure to identify meaningful edge cases based on parameter types and boundary conditions found in the code
Generates real, runnable pytest test files covering happy-path, edge-case, negative, and load scenarios
Runs the generated tests and measures real code coverage using coverage.py

Results (tested on real functions) :
Function	              Description	                  Tests Generated	       Coverage Achieved
calculate_discount	  Pricing logic with validation	           7	                100% (6/6 lines)
is_palindrome	      String processing	                       4	                100% (3/3 lines)
find_max	          List/loop-based logic	                   4	                100% (8/8 lines)

Result: 100% test coverage achieved across 3 structurally different functions (conditionals, string operations, and loops), with 15 total auto-generated test cases and zero manual test writing.

How It Works :

Your Code → AST Parser → Boundary Analyzer → Test Generator → Pytest Writer → Coverage Runner → Results

The tool never guesses blindly — it first extracts structural facts about the code (parameter types, branch conditions) deterministically via AST parsing, then uses that structured data to generate relevant, targeted test cases rather than generic ones.

Tech Stack :
Backend: Python, FastAPI, ast module, pytest, coverage.py
Frontend: React, Vite, Tailwind CSS

Try It Yourself :
Paste any Python function into the input box
Click "Generate Tests"
View the generated test cases and real coverage results

Architecture :

autotest-ai/
├── backend/
│   └── app/
│       ├── main.py       # FastAPI routes
│       ├── parser.py     # AST parsing
│       ├── analyzer.py   # Edge-case detection
│       ├── generator.py  # Test case generation
│       ├── writer.py     # Pytest file writer
│       └── runner.py     # Coverage measurement
└── frontend/
    └── src/
        ├── App.jsx
        └── api.js

Limitations :
Currently supports single-function analysis (multi-function files parse but only the first function is tested)
Works best with type-hinted functions, since type hints drive edge-case suggestions
Test case generation currently uses rule-based logic derived from static analysis rather than a live LLM call

What I Learned :
Building this surfaced a subtle but real bug: uvicorn --reload watches the entire project directory for changes by default, including folders where the app writes generated files at runtime (examples/, generated_tests/). This caused the server to restart mid-request and silently kill coverage subprocess calls. Fixed by scoping the reload watcher to only the source directory (--reload-dir app).