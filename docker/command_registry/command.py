class CommandRegistry:

    def get_commands(self, language: str, entry_point: str):
        language = language.lower()

        commands = {
            "python": [
                ["python", entry_point]
            ],

            "javascript": [
                ["node", entry_point]
            ],

            "typescript": [
                ["tsc", entry_point],
                ["node", entry_point.replace(".ts", ".js")]
            ],

            "java": [
                ["java", entry_point.replace(".java", "")]
            ],

            "go": [
                ["go", "run", entry_point]
            ],

            "php": [
                ["php", entry_point]
            ],

            "ruby": [
                ["ruby", entry_point]
            ],

            "lua": [
                ["lua", entry_point]
            ],

            "perl": [
                ["perl", entry_point]
            ],

            "r": [
                ["Rscript", entry_point]
            ],

            "julia": [
                ["julia", entry_point]
            ],

            "shell": [
                ["sh", entry_point]
            ],

            "powershell": [
                ["pwsh", entry_point]
            ],

            "c": [
                ["gcc", entry_point, "-o", "app"],
                ["./app"]
            ],

            "cpp": [
                ["g++", entry_point, "-o", "app"],
                ["./app"]
            ],

            "rust": [
                ["rustc", entry_point, "-o", "app"],
                ["./app"]
            ],

            "csharp": [
                ["dotnet", "run"]
            ],

            "kotlin": [
                ["kotlinc", entry_point, "-include-runtime", "-d", "main.jar"],
                ["java", "-jar", "main.jar"]
            ],

            "scala": [
                ["scala", entry_point.replace(".scala", "")]
            ],

            "swift": [
                ["swift", entry_point]
            ],

            "dart": [
                ["dart", "run", entry_point]
            ],
        }

        if language not in commands:
            raise ValueError(f"Unsupported language: {language}")

        return commands[language]