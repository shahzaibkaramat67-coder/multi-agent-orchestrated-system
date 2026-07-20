from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Tools.execution_engine.execution_engine import ExecutorEngine
from Tools.execution_engine.models import ExecutionRequest, ExecutionFile

engine = ExecutorEngine()




print("time for go testing")
request = ExecutionRequest(
    language="go",
    entry_point="main.go",
    files=[
        ExecutionFile(
            path="main.go",
            content="""
package main

import "fmt"

func main() {
    fmt.Println("Hello Go")
}
""",
        )
    ],
)



result = engine.execute(request)

print(result)