from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Tools.execution_engine.execution_engine import ExecutorEngine
from Tools.execution_engine.models import ExecutionRequest, ExecutionFile

engine = ExecutorEngine()


request = ExecutionRequest(
    language="typescript",
    entry_point="main.ts",
    files=[
        ExecutionFile(
            path="main.ts",
            content='console.log("Hello TypeScript");',
        )
    ],
)


print("end testing")
result = engine.execute(request)

print(result)