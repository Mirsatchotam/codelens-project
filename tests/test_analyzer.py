
from app.analyzer import analyze_code


def test_detects_function():
    result = analyze_code("def greet(name):\n    print(name)")

    functions = result["code_details"]["functions"]["regular_function"]

    assert len(functions) == 1
    assert functions[0]["name"] == "greet"
    assert functions[0]["line"] == 1


def test_detects_function_call():
    result = analyze_code("print('Hello')")

    calls = result["code_details"]["function_calls"]

    assert len(calls) == 1
    assert calls[0]["name"] == "print"
    assert calls[0]["line"] == 1


def test_detects_syntax_error():
    result = analyze_code("def broken(")

    errors = result["code_details"]["syntax_errors"]

    assert len(errors) == 1
    assert errors[0]["line"] == 1


def test_counts_lines():
    code = "x = 1\n\n# comment\ny = 2"
    result = analyze_code(code)

    overview = result["overview"]

    assert overview["total_lines"] == 4
    assert overview["non_empty_lines"] == 3
    assert overview["comment_lines"] == 1


def test_detects_class_and_method():
    code = """
class Greeter:
    def greet(self):
        self.say_hello()

    def say_hello(self):
        print("Hello")
"""
    result = analyze_code(code)
    details = result["code_details"]

    assert details["classes"][0]["name"] == "Greeter"
    assert len(details["functions"]["regular_function"]) == 2
    assert any(
        call["name"] == "self.say_hello"
        for call in details["method_calls"]
    )


def test_detects_loops_and_conditions():
    code = """
for number in range(3):
    if number > 0:
        print(number)
"""
    result = analyze_code(code)
    details = result["code_details"]

    assert any(loop["type"] == "For" for loop in details["loops"])
    assert any(
        condition["type"] == "If"
        for condition in details["conditions"]
    )


def test_detects_imports():
    code = "import os\nfrom pathlib import Path"
    result = analyze_code(code)

    imports = result["code_details"]["imports"]

    assert len(imports) == 2
    assert imports[0]["type"] == "import"
    assert imports[1]["type"] == "import_from"


def test_detects_async_function():
    code = "async def fetch_data():\n    return 1"
    result = analyze_code(code)

    functions = result["code_details"]["functions"]["async_function"]

    assert len(functions) == 1
    assert functions[0]["name"] == "fetch_data"


def test_detects_nested_function_with_correct_line():
    code = (
        "def outer():\n"
        "    def inner():\n"
        "        return 1\n"
        "    return inner()\n"
    )

    result = analyze_code(code)
    functions = result["code_details"]["functions"]["regular_function"]

    assert functions == [
        {"name": "outer", "line": 1},
        {"name": "inner", "line": 2},
    ]


def test_detects_multiple_classes_in_order():
    code = (
        "class Alpha:\n"
        "    pass\n"
        "\n"
        "class Beta:\n"
        "    pass\n"
    )

    result = analyze_code(code)
    classes = result["code_details"]["classes"]

    assert classes == [
        {"name": "Alpha", "line": 1},
        {"name": "Beta", "line": 4},
    ]


def test_syntax_error_does_not_return_partial_structure():
    code = "def valid():\n    pass\n\ndef broken("
    result = analyze_code(code)
    details = result["code_details"]

    assert len(details["syntax_errors"]) == 1
    assert details["syntax_errors"][0]["line"] == 4
    assert details["functions"]["regular_function"] == []
