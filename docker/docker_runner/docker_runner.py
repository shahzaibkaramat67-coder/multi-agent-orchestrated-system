from image_registry.image_registry import ImageRegistry
from docker.docker_manager.docker_manager import DockerManager
from docker.command_registry.command import CommandRegistry


class DockerRunner:
    def __init__(self):
        self.image_registry = ImageRegistry()
        self.docker_manager = DockerManager()
        self.Command_Registry = CommandRegistry()

    def run(self, workspace, request):
        image = self.image_registry.get_image(request.language)
        Command = self.Command_Registry.get_commands(request.language, request.entry_point)

        # Build the Docker command here (or let DockerManager do it)

        return self.docker_manager.run_container(
            image_name=image,
            workspace=workspace,
            Command=Command,
            timeout=request.timeout,
        )