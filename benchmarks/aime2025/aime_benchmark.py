import json
import re
from pathlib import Path
from typing import Any

from core.base_benchmark import BaseBenchmark
from core.models.task import EvaluationResult, Task


class AIMEBenchmark(BaseBenchmark):
    def __init__(self, data_dir: str | Path | None = None):
        if data_dir is None:
            # Use path relative to this file
            data_dir = Path(__file__).parent / "tasks"
        self.data_dir = Path(data_dir)
        self._tasks = self._load_tasks()

    @property
    def name(self) -> str:
        return "AIME"

    def get_task_ids(self) -> list[str]:
        return list(self._tasks.keys())

    def get_task(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def evaluate(self, task_id: str, output: Any) -> EvaluationResult:
        """Evaluate an output for a given task ID."""
        task = self.get_task(task_id)
        expected = task.data["ground_truth"]
        output_str = str(output).strip() if output is not None else ""

        extracted_numbers = self._extract_numbers(output_str)
        normalized_expected = self._normalize_number(expected)

        if normalized_expected in extracted_numbers:
            return EvaluationResult(score=1.0, score_explanation=f"Correct! Found answer {expected} in output.")

        if extracted_numbers:
            return EvaluationResult(score=0.0, score_explanation=f"Incorrect. Expected {expected}, found: {', '.join(extracted_numbers[:3])}")

        return EvaluationResult(score=0.0, score_explanation=f"Incorrect. Expected {expected}, no valid numbers found in output.")

    def _load_tasks(self) -> dict[str, Task]:
        tasks = {}
        for json_file in self.data_dir.glob("*.json"):
            with open(json_file) as f:
                data = json.load(f)
                task = Task(task_id=data["task_id"], benchmark=self.name, data=data)
                tasks[task.task_id] = task
        return tasks

    def _extract_numbers(self, text: str) -> list[str]:
        patterns = [
            r"\b\d{1,4}\b",  # Simple integers up to 4 digits
            r"\b\d+\.\d+\b",  # Decimals
            r"\b\d+/\d+\b",  # Fractions
        ]

        numbers = []
        for pattern in patterns:
            numbers.extend(re.findall(pattern, text))

        return [self._normalize_number(n) for n in numbers]

    def _normalize_number(self, num_str: str) -> str:
        try:
            if "/" in num_str:
                parts = num_str.split("/")
                if len(parts) == 2 and parts[1] != "0":
                    result = float(parts[0]) / float(parts[1])
                    return str(int(result)) if result.is_integer() else str(result)

            num = float(num_str)
            return str(int(num)) if num.is_integer() else str(num)
        except (ValueError, ZeroDivisionError):
            return num_str

    def get_task_info(self, task_id: str) -> dict[str, Any]:
        """Get additional information about a task."""
        task = self.get_task(task_id)
        metadata = task.data.get("metadata", {})
        return {
            "question": task.data.get("question", ""),
            "ground_truth": task.data.get("ground_truth", ""),
            "source": task.data.get("source", ""),
            "domain": task.data.get("domain", ""),
            "subset": metadata.get("subset", ""),
            "problem_number": metadata.get("problem_number", None),
        }

    def get_tasks_by_subset(self, subset: str) -> list[str]:
        """Get all task IDs for a specific subset (AIME2025-I or AIME2025-II)."""
        return [task_id for task_id, task in self._tasks.items() if task.data.get("metadata", {}).get("subset") == subset]

    def get_problem_numbers(self) -> dict[str, list[int]]:
        """Get problem numbers organized by subset."""
        result = {}
        for task in self._tasks.values():
            metadata = task.data.get("metadata", {})
            subset = metadata.get("subset", "Unknown")
            problem_num = metadata.get("problem_number")
            if problem_num:
                if subset not in result:
                    result[subset] = []
                result[subset].append(problem_num)

        # Sort problem numbers for each subset
        for subset in result:
            result[subset].sort()

        return result
