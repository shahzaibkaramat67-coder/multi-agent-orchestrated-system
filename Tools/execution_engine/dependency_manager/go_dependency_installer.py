import subprocess
from pathlib import Path


class GoDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        go_mod = workspace / "go.mod"

        if not go_mod.exists():
            return

        subprocess.run(
            [
                "go",
                "mod",
                "tidy",
            ],
            cwd=workspace,
            check=True,
        )
