import os
from pathlib import Path
import tempfile


class ProjectBuilder:
    def create_workspace(self):
        temp_directory = tempfile.mkdtemp()
        workspace = Path(temp_directory)
        print(workspace)
        return workspace
