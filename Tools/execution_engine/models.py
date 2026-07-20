from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExecutionFile:
    path: str = ""
    content: str = ""


@dataclass
class ExecutionRequest:
    language: str = ""
    files: list[ExecutionFile] = field(default_factory=list)
    entry_point: str = ""
    timeout: int = 10
    working_directory: Optional[str] = None
    environment_variables: dict[str, str] = field(default_factory=dict)


@dataclass
class ExecutionResult:
    success: bool
    language: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    execution_time: float = 0.0
    working_directory: Optional[str] = None
    executable_path: Optional[str] = None
    error_message: Optional[str] = None
