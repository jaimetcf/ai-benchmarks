from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    """
    Flexible task representation that can accommodate any benchmark structure.

    Essential fields:
    - task_id: Unique identifier for the task
    - benchmark: Name of the benchmark this task belongs to
    - data: Flexible field that can contain any task-specific data structure

    The data field replaces the previous rigid problem/expected_answer/metadata structure
    and allows each benchmark to define its own data format.
    """

    task_id: str
    benchmark: str
    data: dict[str, Any] = field(default_factory=dict)

    # Convenient accessors for common task data
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the task data."""
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access to task data."""
        return self.data[key]

    def __contains__(self, key: str) -> bool:
        """Check if key exists in task data."""
        return key in self.data

    def keys(self):
        """Get all keys from task data."""
        return self.data.keys()

    def items(self):
        """Get all items from task data."""
        return self.data.items()

    # Convenient methods for common operations
    def update(self, other_data: dict[str, Any]) -> None:
        """Update task data with new values."""
        self.data.update(other_data)

    def copy(self) -> "Task":
        """Create a copy of this task."""
        return Task(task_id=self.task_id, benchmark=self.benchmark, data=self.data.copy())


@dataclass
class ExecutionResult:
    """The direct output from a sandboxed code execution."""

    execution_output: Any | None = None
    execution_trace: str | None = None
    error: str | None = None
    execution_time: float | None = None


@dataclass
class EvaluationResult:
    """The result of scoring an execution against a benchmark task."""

    score: float = 0.0
    score_explanation: str | None = None


@dataclass
class TaskResult:
    """The complete result of running a gene against a single benchmark task."""

    task_id: str
    benchmark_name: str
    execution: ExecutionResult
    evaluation: EvaluationResult | None = None
