import subprocess
from pathlib import Path


class RubyDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        gemfile = workspace / "Gemfile"

        if not gemfile.exists():
            return

        subprocess.run(
            [
                "bundle",
                "install",
            ],
            cwd=workspace,
            check=True,
        )
