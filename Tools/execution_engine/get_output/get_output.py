from models import ExecutionResult


class OutputHandler:

    def get_output(
        self,
        process,
        language: str,
        execution_time: float,
        working_directory: str,
    ) -> ExecutionResult:

        return ExecutionResult(
            success=process.returncode == 0,
            language=language,
            stdout=process.stdout,
            stderr=process.stderr,
            exit_code=process.returncode,
            execution_time=execution_time,
            working_directory=working_directory,
            executable_path=None,
            error_message=None if process.returncode == 0 else process.stderr,
        )
