from abc import ABC, abstractmethod

from .models import ExecutionRequest, ExecutionResult


class BaseExecutor(ABC):

    @abstractmethod
    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        pass
