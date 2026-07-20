from ..base_executor import BaseExecutor
from ..models import ExecutionRequest, ExecutionResult
from ..project_builder.project_builder import ProjectBuilder
from ..file_manager.file_manager import FileManager
from ..dependency_manager.no_dependency_installer import NoDependencyInstaller
from ..Cleaner.cleanup import Cleaner
from docker.docker_runner.docker_runner import DockerRunner
from ..get_output.get_output import OutputHandler
import time
# from docker.docker_runner import docker_runner




class CExecutors(BaseExecutor):
    def __init__(self):
        self.project_builder = ProjectBuilder()
        self.file_manager = FileManager()
        self.dependency_installer = NoDependencyInstaller()
        self.cleaner = Cleaner()
        self.docker_runner = DockerRunner()
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
            process = self.docker_runner.run(workspace, request)
            end = time.perf_counter()
            print("process", process)
            execution_time = end - start
            result = self.get_output.get_output(process, request.language, execution_time, str(workspace))
            print("result", result)
            return result
        finally:
             self.cleaner.cleanup(workspace)
#   language: str,
#         execution_time: float,
#         working_directory: str,