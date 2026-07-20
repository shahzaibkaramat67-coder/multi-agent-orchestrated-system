import subprocess
from pathlib import Path


class RustDependencyInstaller:

    def install(
        self,
        workspace: Path,
    ):

        cargo = workspace / "Cargo.toml"

        if not cargo.exists():
            return

        subprocess.run(
            [
                "cargo",
                "build",
            ],
            cwd=workspace,
            check=True,
        )
