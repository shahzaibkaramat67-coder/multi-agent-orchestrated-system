import subprocess
from pathlib import Path


class PhpDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        composer = workspace / "composer.json"

        if not composer.exists():
            return

        subprocess.run(
            [
                "composer",
                "install",
            ],
            cwd=workspace,
            check=True,
        )
