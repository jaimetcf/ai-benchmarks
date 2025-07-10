from numbers import Number
from pathlib import Path
from typing import Any
import json
import re

from core.base_benchmark import BaseBenchmark
from core.models.task import EvaluationResult, Task


class GSM8KBenchmark(BaseBenchmark):
    """Benchmark for evaluating grade school math word problems."""

    def __init__(self, data_dir: str | Path | None = None):
        """Initialize the benchmark.
        
        Args:
            data_dir: Optional path to data directory. If None, uses default.
        """
        if data_dir is None:
            data_dir = Path(__file__).parent / "data"
        self.data_dir = Path(data_dir)
        self._tasks = self._load_tasks()

    @property
    def name(self) -> str:
        """Return the benchmark name."""
        return "GSM8K"

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
            output: The model's output
            
        Returns:
            EvaluationResult with score and explanation
        """
        task = self.get_task(task_id)
        correct_answer = task.data["answer"].strip()
        correct_number = self._match_answer_number(correct_answer)
        predicted_number = self._match_answer_number(output)

        if predicted_number == correct_number:
            return EvaluationResult(
                score=1.0, 
                score_explanation="Correct answer")
        else:
            return EvaluationResult(
                score=0.0, 
                score_explanation=f"Expected: {correct_number}, Got: {predicted_number}")

    def _match_answer_number(self, output: str) -> str | None:
        """Match the answer number in the output."""
        match = re.search(r"####\s*([\d\.\-]+)", str(output))
        if match:
            return match.group(1).strip()
        return None

    def _load_tasks(self) -> dict[str, Task]:
        """Load tasks from the test.jsonl file."""
        tasks = {}
        data_file = self.data_dir / "test.jsonl"
        with open(data_file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                data = json.loads(line)
                task_id = f"{idx:04d}"
#                task_id = f"gsm8k_{idx:04d}"
                task = Task(
                    task_id=task_id,
                    benchmark=self.name,
                    data={
                        "question": data["question"],
                        "answer": data["answer"]
                    }
                )
                tasks[task_id] = task
        return tasks