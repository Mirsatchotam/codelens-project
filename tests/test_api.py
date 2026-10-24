
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to CodeLens"


def test_analyze_valid_code():
    response = client.post(
        "/analyze",
        json={"code": "def greet(name):\n    print(name)"},
    )

    assert response.status_code == 200

    data = response.json()
    functions = data["code_details"]["functions"]["regular_function"]

    assert functions[0]["name"] == "greet"


def test_analyze_syntax_error():
    response = client.post(
        "/analyze",
        json={"code": "def broken("},
    )

    assert response.status_code == 200

    data = response.json()
    assert len(data["code_details"]["syntax_errors"]) == 1


def test_analyze_empty_code():
    response = client.post(
        "/analyze",
        json={"code": ""},
    )

    assert response.status_code == 422
