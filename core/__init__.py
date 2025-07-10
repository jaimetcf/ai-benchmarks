"""Core benchmark interfaces and models."""

from core.base_benchmark import BaseBenchmark, CodeExecutionBenchmark
from core.model import Model
from core.models.task import EvaluationResult, ExecutionResult, Task, TaskResult

__all__ = [
    "BaseBenchmark",
    "CodeExecutionBenchmark",
    "Model",
    "Task",
    "TaskResult",
    "EvaluationResult",
    "ExecutionResult",
]
