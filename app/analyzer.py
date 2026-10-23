
import ast
import tokenize
from io import BytesIO


def count_comment_lines(code: str) -> int:
    """Count lines containing Python comment tokens."""
    comment_lines = set()

    try:
        tokens = tokenize.tokenize(
            BytesIO(code.encode("utf-8")).readline
        )

        for token in tokens:
            if token.type == tokenize.COMMENT:
                comment_lines.add(token.start[0])

    except (tokenize.TokenError, IndentationError):
        pass

    return len(comment_lines)


def analyze_code(code: str) -> dict:
    """Analyze Python source code and return its structural details."""
    lines = code.splitlines()

    result = {
        "code_details": {
            "functions": {
                "regular_function": [],
                "async_function": [],
            },
            "syntax_errors": [],
            "loops": [],
            "conditions": [],
            "imports": [],
            "function_calls": [],
            "method_calls": [],
            "classes": [],
        },
        "overview": {
            "total_lines": len(lines),
            "non_empty_lines": sum(
                1 for line in lines if line.strip()
            ),
            "comment_lines": count_comment_lines(code),
        },
    }

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        result["code_details"]["syntax_errors"].append(
            {
                "message": error.msg,
                "line": error.lineno,
                "column": error.offset,
            }
        )
        return result

    details = result["code_details"]

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            details["functions"]["regular_function"].append({
                "name": node.name,
                "line": node.lineno,
            })

        elif isinstance(node, ast.AsyncFunctionDef):
            details["functions"]["async_function"].append({
                "name": node.name,
                "line": node.lineno,
            })

        elif isinstance(node, ast.ClassDef):
            details["classes"].append({
                "name": node.name,
                "line": node.lineno,
            })

        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            details["loops"].append({
                "type": type(node).__name__,
                "line": node.lineno,
            })

        elif isinstance(node, (ast.If, ast.IfExp)):
            details["conditions"].append({
                "type": type(node).__name__,
                "line": node.lineno,
            })

        elif isinstance(node, ast.Import):
            details["imports"].append({
                "type": "import",
                "names": [alias.name for alias in node.names],
                "line": node.lineno,
            })

        elif isinstance(node, ast.ImportFrom):
            details["imports"].append({
                "type": "import_from",
                "module": node.module,
                "names": [alias.name for alias in node.names],
                "line": node.lineno,
            })

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                details["function_calls"].append({
                    "name": node.func.id,
                    "line": node.lineno,
                })

            elif isinstance(node.func, ast.Attribute):
                details["method_calls"].append({
                    "name": ast.unparse(node.func),
                    "line": node.lineno,
                })

    for key, value in details.items():
        if isinstance(value, list):
            value.sort(key=lambda item: item.get("line") or 0)

    for value in details["functions"].values():
        value.sort(key=lambda item: item["line"])

    return result
