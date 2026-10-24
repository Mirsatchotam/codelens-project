from pydantic import BaseModel, Field


class CodeAnalysisRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=100_000,
        description="Python source code to analyze",
    )


class CodeAnalysisResponse(BaseModel):
    code_details: dict
    overview: dict