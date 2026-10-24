
from pydantic import BaseModel, Field


class CodeAnalysisRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=100_000,
        description="Python source code to analyze",
    )


class SyntaxErrorDetail(BaseModel):
    message: str
    line: int | None
    column: int | None


class NamedLocation(BaseModel):
    name: str
    line: int

class FunctionLocation(NamedLocation):
    complexity: int = Field(ge=1)
    complexity_level: str

class LoopDetail(BaseModel):
    type: str
    line: int


class ConditionDetail(BaseModel):
    type: str
    line: int


class ImportDetail(BaseModel):
    type: str
    line: int
    names: list[str]
    module: str | None = None


class FunctionDetails(BaseModel):
    regular_function: list[FunctionLocation]
    async_function: list[FunctionLocation]


class FunctionCallDetail(BaseModel):
    name: str
    line: int


class MethodCallDetail(BaseModel):
    name: str
    line: int


class CodeDetails(BaseModel):
    functions: FunctionDetails
    syntax_errors: list[SyntaxErrorDetail]
    loops: list[LoopDetail]
    conditions: list[ConditionDetail]
    imports: list[ImportDetail]
    function_calls: list[FunctionCallDetail]
    method_calls: list[MethodCallDetail]
    classes: list[NamedLocation]
    long_functions: list[LongFunctionDetail]


class CodeOverview(BaseModel):
    total_lines: int
    non_empty_lines: int
    comment_lines: int


class CodeAnalysisResponse(BaseModel):
    code_details: CodeDetails
    overview: CodeOverview

class LongFunctionDetail(BaseModel):
    name: str
    line: int
    length: int