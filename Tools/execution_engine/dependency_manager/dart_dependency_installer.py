import subprocess
from pathlib import Path


class DartDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        pubspec = workspace / "pubspec.yaml"

        if not pubspec.exists():
            return

        subprocess.run(
            [
                "dart",
                "pub",
                "get",
            ],
            cwd=workspace,
            check=True,
        )
