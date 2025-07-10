from abc import ABC, abstractmethod
from typing import Any

from core.models.task import EvaluationResult, Task, TaskResult


class BaseBenchmark(ABC):
    """Base class for benchmark implementations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Benchmark name."""
        pass

    @abstractmethod
    def get_task_ids(self) -> list[str]:
        """Get all task IDs for this benchmark."""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        """Get a task object by its ID."""
        pass

    @abstractmethod
    def evaluate(self, task_id: str, output: Any) -> EvaluationResult:
        """
        Evaluate an output for a given task, returning an EvaluationResult.

        This is the simple evaluation interface for benchmarks that don't require
        code execution (e.g., AIME, GAIA).

        Args:
            task_id: The ID of the task to evaluate
            output: The model's output/answer

        Returns:
            EvaluationResult with score and explanation
        """
        pass


# TODO: this is a patch on not having the right pattern for BaseBenchmark. should iterate on this.
class CodeExecutionBenchmark(BaseBenchmark):
    """
    Extended base class for benchmarks that require code execution.

    This class is for benchmarks like SWE-bench that need to execute code
    and run tests, rather than just comparing answers.
    """

    @abstractmethod
    def evaluate_with_execution(self, task_id: str, output: Any, **kwargs) -> TaskResult:
        """
        Evaluate an output that requires execution (e.g., code patches).

        Args:
            task_id: The ID of the task to evaluate
            output: The model's output (e.g., code patch)
            **kwargs: Additional execution parameters (e.g., use_modal, timeout)

        Returns:
            TaskResult with full execution details and evaluation
        """
        pass

    def evaluate(self, task_id: str, output: Any) -> EvaluationResult:
        """
        Simple evaluation interface that delegates to evaluate_with_execution.

        This provides compatibility with the base interface while using the
        execution-based evaluation internally.
        """
        result = self.evaluate_with_execution(task_id, output)
        if result.evaluation:
            return result.evaluation
        else:
            # If no evaluation result, create one from execution status
            return EvaluationResult(score=0.0, score_explanation=f"Execution failed: {result.execution.error or 'Unknown error'}")
