import subprocess
from pathlib import Path


class DotnetDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        subprocess.run(
            [
                "dotnet",
                "restore",
            ],
            cwd=workspace,
            check=True,
        )
