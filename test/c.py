from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Tools.execution_engine.execution_engine import ExecutorEngine
from Tools.execution_engine.models import ExecutionRequest, ExecutionFile

engine = ExecutorEngine()


print("time for c testing")

request = ExecutionRequest(
    language="c",
    entry_point="main.c",
    files=[
        ExecutionFile(
            path="main.c",
            content="""
#include <stdio.h>

int main() {
    printf("Hello C\\n");
    return 0;
}
""",
        )
    ],
)

result = engine.execute(request)

print(result)