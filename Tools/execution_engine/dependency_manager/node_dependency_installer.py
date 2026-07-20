import subprocess
from pathlib import Path


class NodeDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        package = workspace / "package.json"

        if not package.exists():
            return

        subprocess.run(
            [
                "npm",
                "install",
            ],
            cwd=workspace,
            check=True,
        )
