from pathlib import Path
from models import ExecutionFile


class FileManager:
    def write_files(
        self,
        workspace: Path,
        files: list[ExecutionFile],
    ) -> None:

        for file in files:

            file_path = workspace / file.path

            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(file.content)
