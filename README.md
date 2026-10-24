# CodeLens

**CodeLens is a Python source code analyzer built with FastAPI and Python's Abstract Syntax Tree (AST).** It analyzes Python code, identifies structural elements, measures function complexity, and reports potentially long functions.

## Features

- **Function detection** — identifies regular and asynchronous functions with their names and line numbers.
- **Cyclomatic complexity** — calculates a complexity score for each function.
- **Complexity classification** — categorizes functions as `low`, `moderate`, `high`, or `very_high`.
- **Long function detection** — identifies functions occupying more than 50 source lines.
- **Class detection** — finds class definitions and their line numbers.
- **Control flow analysis** — detects loops and conditional expressions.
- **Import analysis** — identifies `import` and `from ... import ...` statements.
- **Call analysis** — detects function calls and method calls.
- **Syntax error reporting** — returns syntax error messages with line and column information.
- **Code statistics** — reports total lines, non-empty lines, and lines containing comments.
- **REST API** — exposes analysis functionality through FastAPI.
- **Automated tests** — tests the analyzer and API using pytest.

## Tech Stack

- **Python** — core language
- **FastAPI** — REST API
- **Pydantic** — request validation and response schemas
- **AST (`ast`)** — Python source code parsing and structural analysis
- **`tokenize`** — comment detection
- **pytest** — automated testing

## Project Structure

```text
CodeLens/
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   ├── test_analyzer.py
│   └── test_api.py
├── README.md
└── requirements.txt
```

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Mirsatchotam/codelens-project.git
cd codelens-project
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- **API root:** http://127.0.0.1:8000/
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **OpenAPI schema:** http://127.0.0.1:8000/openapi.json

## Usage

Send a `POST` request to `/analyze` with Python source code in the request body.

### Example request

```json
{
  "code": "def classify(n):\n    if n > 0:\n        return 'positive'\n    return 'non-positive'"
}
```

### Example response

The following is a shortened example of the response structure:

```json
{
  "code_details": {
    "functions": {
      "regular_function": [
        {
          "name": "classify",
          "line": 1,
          "complexity": 2,
          "complexity_level": "low"
        }
      ],
      "async_function": []
    },
    "syntax_errors": [],
    "loops": [],
    "conditions": [
      {
        "type": "If",
        "line": 2
      }
    ],
    "imports": [],
    "function_calls": [],
    "method_calls": [],
    "classes": [],
    "long_functions": []
  },
  "overview": {
    "total_lines": 4,
    "non_empty_lines": 4,
    "comment_lines": 0
  }
}
```

The response includes structural details and code statistics. The exact result depends on the submitted source code.

## Complexity Metrics

CodeLens uses a simplified cyclomatic complexity calculation:

\[
M = 1 + D
\]

Where:

- \(M\) is cyclomatic complexity.
- \(D\) is the number of decision points detected by the analyzer.

The current implementation counts conditional statements, loops, exception handlers, and additional operands in Boolean expressions.

| Complexity | Classification |
|---:|---|
| 1–5 | `low` |
| 6–10 | `moderate` |
| 11–20 | `high` |
| 21+ | `very_high` |

These thresholds are configurable design choices, not universal quality standards.

## Run Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The tests cover source code analysis, syntax errors, nested functions, complexity calculations, long function detection, and API behavior.

## Limitations

- CodeLens analyzes Python source code without executing it.
- Cyclomatic complexity is a simplified metric and may differ from specialized static analysis tools.
- The long-function threshold is currently fixed at more than 50 source lines.
- The analyzer is not a complete static analysis, type-checking, or security auditing tool.
- The project is under active development.

## Roadmap

Potential future improvements include:

- Configurable analysis thresholds
- Duplicate code detection
- Cognitive complexity metrics
- More edge-case and integration tests
- Improved diagnostics and reporting
- Deployment and CI automation

## License

No license has been specified yet. Add a license before distributing the project for reuse.
