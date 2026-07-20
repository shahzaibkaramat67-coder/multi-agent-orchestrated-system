class ImageRegistry:
    def __init__(self):
        self.images = {
            "python": "python-executor",
            "javascript": "javascript-executor",
            "typescript": "typescript-executor",
            "java": "java-executor",
            "c": "c-executor",
            "cpp": "cpp-executor",
            "csharp": "csharp-executor",
            "go": "go-executor",
            "rust": "rust-executor",
            "php": "php-executor",
            "ruby": "ruby-executor",
            "kotlin": "kotlin-executor",
            "swift": "swift-executor",
            "scala": "scala-executor",
            "dart": "dart-executor",
            "lua": "lua-executor",
            "perl": "perl-executor",
            "r": "r-executor",
            "julia": "julia-executor",
            "shell": "shell-executor",
            "powershell": "powershell-executor",
        }

    def get_image(self, language: str):
        return self.images.get(language.lower())