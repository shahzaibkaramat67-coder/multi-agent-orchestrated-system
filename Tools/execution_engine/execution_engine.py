from .executor_registry import ExecutorRegistry

from .models import ExecutionRequest
from .models import ExecutionResult
import subprocess
from .executors.python_executor import PythonExecutor
from .executors.node_executor import NodeExecutor
from .executors.typescript_executor import TypeScriptExecutor
from .executors.java_executor import JavaExecutor
from .executors.c_executor import CExecutors
from .executors.cpp_executor import CppExecutor
from .executors.csharp_executor import CSharpExecutor
from .executors.go_executor import GoExecutor
from .executors.rust_executor import RustExecutor
from .executors.php_executor import PhpExecutor
from .executors.ruby_executor import RubyExecutor
from .executors.kotlin_executor import KotlinExecutor
from .executors.swift_executor import SwiftExecutor
from .executors.scala_executor import ScalaExecutor
from .executors.dart_executor import DartExecutor
from .executors.lua_executor import LuaExecutor
from .executors.perl_executor import PerlExecutor
from .executors.r_executor import RExecutor
from .executors.julia_executor import JuliaExecutor
from .executors.shell_executor import ShellExecutor
from .executors.powershell_executor import PowerShellExecutor

# from executors.python_executor import PythonExecutor
# from executors.node_executor import NodeExecutor
# from executors.typescript_executor import TypeScriptExecutor
# from executors.java_executor import JavaExecutor
# from executors.c_executor import CExecutors
# from executors.cpp_executor import CppExecutor
# from executors.csharp_executor import CSharpExecutor
# from executors.go_executor import GoExecutor
# from executors.rust_executor import RustExecutor
# from executors.php_executor import PhpExecutor
# from executors.ruby_executor import RubyExecutor
# from executors.kotlin_executor import KotlinExecutor
# from executors.swift_executor import SwiftExecutor
# from executors.scala_executor import ScalaExecutor
# from executors.dart_executor import DartExecutor
# from executors.lua_executor import LuaExecutor
# from executors.perl_executor import PerlExecutor
# from executors.r_executor import RExecutor
# from executors.julia_executor import JuliaExecutor
# from executors.shell_executor import ShellExecutor
# from executors.powershell_executor import PowerShellExecutor

class ExecutorEngine:
    def __init__(self):
        self.registry = ExecutorRegistry()

        self.register_executors()

    def register_executors(self):

            self.registry.register(
                "python",
                PythonExecutor(),
            )

            self.registry.register(
                "javascript",
                NodeExecutor(),
            )

            self.registry.register(
                "typescript",
                TypeScriptExecutor(),
            )

            self.registry.register(
                "java",
                JavaExecutor(),
            )

            self.registry.register(
                "c",
                CExecutors(),
            )

            self.registry.register(
                "cpp",
                CppExecutor(),
            )

            self.registry.register(
                "csharp",
                CSharpExecutor(),
            )

            self.registry.register(
                "go",
                GoExecutor(),
            )

            self.registry.register(
                "rust",
                RustExecutor(),
            )

            self.registry.register(
                "php",
                PhpExecutor(),
            )

            self.registry.register(
                "ruby",
                RubyExecutor(),
            )

            self.registry.register(
                "kotlin",
                KotlinExecutor(),
            )

            self.registry.register(
                "swift",
                SwiftExecutor(),
            )

            self.registry.register(
                "scala",
                ScalaExecutor(),
            )

            self.registry.register(
                "dart",
                DartExecutor(),
            )

            self.registry.register(
                "lua",
                LuaExecutor(),
            )

            self.registry.register(
                "perl",
                PerlExecutor(),
            )

            self.registry.register(
                "r",
                RExecutor(),
            )

            self.registry.register(
                "julia",
                JuliaExecutor(),
            )

            self.registry.register(
                "shell",
                ShellExecutor(),
            )

            self.registry.register(
                "powershell",
                PowerShellExecutor(),
)
    def execute(
        self,
        request: ExecutionRequest,
    ):
        try:
            executor = self.registry.get_executor(request.language.lower())
            return executor.execute(request)
        except subprocess.TimeoutExpired as e:
            return ExecutionResult(
                success=False,
                language=request.language,
                stderr=str(e),
                exit_code=-1,
                error_message="Execution timed out.",
            )

        except FileNotFoundError as e:
            return ExecutionResult(
                success=False,
                language=request.language,
                stderr=str(e),
                exit_code=-1,
                error_message="Compiler or interpreter not found.",
            )

        except ValueError as e:
            return ExecutionResult(
                success=False,
                language=request.language,
                stderr=str(e),
                exit_code=-1,
                error_message=str(e),
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                language=request.language,
                stderr=str(e),
                exit_code=-1,
                error_message=f"Unexpected error: {str(e)}",
            )
                    
            
            


# import tempfile
# import subprocess
# import os


# def code_executor_Tool(Sub_code_agent_result):
#     """
#     Executes Python code safely in a temporary file.
#     Returns execution result.
#     """
#     try:
#         with tempfile.NamedTemporaryFile(
#             mode="w", suffix=".py", encoding="utf-8", delete=False
#         ) as temp_file:
#             temp_file.write(Sub_code_agent_result)
#             tem_path = temp_file.name
#             print("tem_path from code executer tool", tem_path)

#         result = subprocess.run(
#             ["python", tem_path], timeout=10, text=True, capture_output=True
#         )
#         os.remove(tem_path)

#         return {
#             "status": "success",
#             "stdout": result.stdout,
#             "stderr": None,
#         }

#     except subprocess.TimeoutExpired:
#         return {"status": "failed", "stdout": "", "stderr": "Execution Timeout"}
#     except Exception as e:
#         return {
#             "status": "failed",
#             "stdout": result.stdout,
#             "stderr": result.stderr,
#         }
