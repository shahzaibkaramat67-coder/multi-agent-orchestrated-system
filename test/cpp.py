from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Tools.execution_engine.execution_engine import ExecutorEngine
from Tools.execution_engine.models import ExecutionRequest, ExecutionFile

engine = ExecutorEngine()




print("time for cpp testing")
request = ExecutionRequest(
    language="cpp",
    entry_point="main.cpp",
    files=[
        ExecutionFile(
            path="main.cpp",
            content="""
#include <iostream>

int main() {
    std::cout << "Hello C++";
    return 0;
}
""",
        )
    ],
)



print("end testing")
result = engine.execute(request)

print(result)