import subprocess


class DockerManager:

    def run_container(
        self,
        image_name: str,
        workspace: str,
        commands: list,
        timeout: int ,
    ):

        last_process = None

        for command in commands:

            docker_command = [
                "docker",
                "run",
                "--rm",

                "-v",
                f"{workspace}:/workspace",

                "-w",
                "/workspace",

                image_name,

                *command,
            ]

            last_process = subprocess.run(
                docker_command,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if last_process.returncode != 0:
                break

        return last_process