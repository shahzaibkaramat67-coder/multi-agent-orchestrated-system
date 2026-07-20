from pathlib import Path
import shutil


class Cleaner:
    def cleanup(self, workspace: Path) -> None:
        shutil.rmtree(workspace)
