from pathlib import Path
import json
import re

from core.base_benchmark import BaseBenchmark
from core.models.task import EvaluationResult, Task
from .utils.code_comparer import CodeComparer


class MLBenchBenchmark(BaseBenchmark):
    """Benchmark for evaluating machine learning code generation tasks."""

    def __init__(self, data_dir: str | Path | None = None):
        """Initialize the benchmark.
        
        Args:
            data_dir: Optional path to data directory. If None, uses default.
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        self.data_dir = Path(data_dir)
        self._tasks = self._load_tasks()
        self.code_comparer = CodeComparer()

    @property
    def name(self) -> str:
        """Return the benchmark name."""
        return "ml_bench"

    def get_task_ids(self) -> list[str]:
        """Return all task IDs."""
        return list(self._tasks.keys())

    def get_task(self, task_id: str) -> Task:
        """Return a task by ID."""
        if task_id not in self._tasks:
            raise ValueError(f"Task {task_id} not found")
        return self._tasks[task_id]

    def evaluate(self, task_id: str, output: str) -> EvaluationResult:
        """Evaluate one model's output for a given task ID.
        
        Args:
            task_id: The task ID to evaluate
            output: The model's output (generated code)
            
        Returns:
            EvaluationResult with score and explanation
        """
        task = self.get_task(task_id)
        ground_truth = task.data["output"].strip()
        generated_code = output.strip()

        result = self.code_comparer.compare(generated_code, ground_truth, task.data["type"])
        
        if result["sameResult"]:
            return EvaluationResult(
                score=1.0, 
                score_explanation=result["reason"])
        else:
            return EvaluationResult(
                score=0.0, 
                score_explanation=result["reason"])

    def _load_tasks(self) -> dict[str, Task]:
        """Load tasks from the test.jsonl file."""
        tasks = {}
        data_file = self.data_dir / "test.jsonl"
        with open(data_file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                task_id = f"{idx:04d}"
                
                task = Task(
                    task_id=task_id,
                    benchmark=self.name,
                    data={
                        "instruction": data["instruction"],
                        "oracle": data["oracle"],
                        "output": data["output"],
                        "type": data.get("type", ""),
                        "arguments": data.get("arguments", ""),
                        "prefix_code": data.get("prefix_code", ""),
                        "github": data.get("github", ""),
                        "path": data.get("path", ""),
                        "id": data.get("id", idx)
                    }
                )
                tasks[task_id] = task
        return tasks 