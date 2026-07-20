from ..base_executor import BaseExecutor
from ..models import ExecutionRequest, ExecutionResult
from ..project_builder.project_builder import ProjectBuilder
from ..file_manager.file_manager import FileManager
from ..dependency_manager.python_dependency_installer import PythonDependencyInstaller
from ..Cleaner.cleanup import Cleaner
from ....docker.docker_runner.docker_runner import DockerRunner
from ..get_output.get_output import OutputHandler
import time


class PythonExecutor(BaseExecutor):
    def __init__(self):
        self.project_builder = ProjectBuilder()
        self.file_manager = FileManager()
        self.dependency_installer = PythonDependencyInstaller()
        self.cleaner = Cleaner()
        self.docker_DockerRunner = DockerRunner()
        self.get_output = OutputHandler()

    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:

        workspace = self.project_builder.create_workspace()
        print("workspace", workspace)
        try:
            self.file_manager.write_files(workspace, request.files)
            self.dependency_installer.install(workspace)
            start = time.perf_counter()
            process = self.docker_DockerRunner.run(workspace, request)
            end = time.perf_counter()
            execution_time = end - start
            print("process", process)
            result = self.get_output.get_output(process, request.language, execution_time, str(workspace))
            print("result", result)
            return result
        finally:
            self.cleaner.cleanup(workspace)
