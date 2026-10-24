
from fastapi import FastAPI

from app.analyzer import analyze_code
from app.schemas import CodeAnalysisRequest, CodeAnalysisResponse

app = FastAPI(
    title="CodeLens",
    description="A Python source code analyzer",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to CodeLens",
        "docs": "/docs",
    }


@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_python_code(request: CodeAnalysisRequest):
    return analyze_code(request.code)
