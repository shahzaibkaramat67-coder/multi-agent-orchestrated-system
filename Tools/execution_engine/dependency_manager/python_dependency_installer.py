import subprocess
from pathlib import Path


class PythonDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        requirements = workspace / "requirements.txt"

        if not requirements.exists():
            return

        subprocess.run(
            [
                "pip",
                "install",
                "-r",
                "requirements.txt",
            ],
            cwd=workspace,
            check=True,
        )
