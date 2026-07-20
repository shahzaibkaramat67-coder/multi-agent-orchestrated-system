from typing import Dict

from .base_executor import BaseExecutor


class ExecutorRegistry:

    def __init__(self):
        self.executors: Dict[str, BaseExecutor] = {}

    def register(self, language: str, executor: BaseExecutor):
        self.executors[language.lower()] = executor

    def get_executor(self, language: str):
        return self.executors[language]
