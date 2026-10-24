# CodeLens

**CodeLens** is a Python source code analyzer built with Python's AST module and FastAPI.

It analyzes Python source code without executing it and returns a structured JSON report.

## Features

- Detects regular and asynchronous functions
- Detects classes, loops, and conditional expressions
- Extracts imports and function or method calls
- Reports syntax errors with line and column information
- Calculates total, non-empty, and comment line counts
- Provides a REST API with request validation and typed response schemas
- Includes automated tests for the analyzer and API

## Tech Stack

- Python
- FastAPI
- Pydantic
- Python AST and `tokenize`
- pytest

## Project Structure

```text
app/
├── analyzer.py
├── main.py
├── schemas.py
└── __init__.py
tests/
├── test_analyzer.py
└── test_api.py
```

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the packages:

```bash
pip install fastapi uvicorn pytest httpx
```

## Run the API

From the project root, run:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

## Example Request

Send a `POST` request to `/analyze` with this JSON body:

```json
{
  "code": "def greet(name):\n    print(name)"
}
```

The response includes detected functions, calls, syntax errors, and code statistics.

## Run Tests

```bash
python -m pytest -v
```

## Current Scope and Limitations

CodeLens currently performs structural analysis of Python source code. It does not execute submitted code, and it is not yet a full static-analysis or security-auditing tool.

## Roadmap

- Expand test coverage for edge cases
- Improve analysis of nested and complex Python expressions
- Add complexity metrics
- Improve error reporting and API documentation
- Add deployment instructions and a hosted demo
