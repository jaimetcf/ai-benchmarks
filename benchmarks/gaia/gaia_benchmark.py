import json
from pathlib import Path
from typing import Any

from core.base_benchmark import BaseBenchmark
from core.models.task import EvaluationResult, Task


class GAIABenchmark(BaseBenchmark):
    def __init__(self, data_dir: str | Path | None = None):
        if data_dir is None:
            # Use path relative to this file
            data_dir = Path(__file__).parent / "files" / "2023"
        self.data_dir = Path(data_dir)
        self._tasks = self._load_tasks()

    @property
    def name(self) -> str:
        return "GAIA"

    def get_task_ids(self) -> list[str]:
        return list(self._tasks.keys())

    def get_task(self, task_id: str) -> Task:
        return self._tasks[task_id]

    def evaluate(self, task_id: str, output: Any) -> EvaluationResult:
        """Evaluate an output for a given task ID."""
        task = self.get_task(task_id)
        expected = task.data["Final answer"]
        output_str = str(output).strip() if output is not None else ""

        # GAIA evaluation is case-sensitive and exact match based on the metadata
        # Some answers may need normalization (e.g., numbers, lists)
        normalized_output = self._normalize_answer(output_str)
        normalized_expected = self._normalize_answer(expected)

        if normalized_output == normalized_expected:
            return EvaluationResult(score=1.0, score_explanation=f"Correct! Answer matches expected: {expected}")

        # Check for partial matches or close answers
        partial_score = self._check_partial_match(normalized_output, normalized_expected, task)
        if partial_score > 0:
            return EvaluationResult(score=partial_score, score_explanation=f"Partial match. Expected: {expected}, Got: {output_str}")

        return EvaluationResult(score=0.0, score_explanation=f"Incorrect. Expected: {expected}, Got: {output_str}")

    def _load_tasks(self) -> dict[str, Task]:
        """Load tasks from metadata.jsonl files."""
        tasks = {}

        # Load from both validation and test sets if they exist
        for subset in ["validation", "test"]:
            metadata_path = self.data_dir / subset / "metadata.jsonl"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    for line in f:
                        data = json.loads(line.strip())
                        task_id = data["task_id"]

                        # Add file paths for any associated files
                        if data.get("file_name"):
                            data["file_path"] = str(self.data_dir / subset / data["file_name"])

                        # Add subset information
                        data["subset"] = subset

                        task = Task(task_id=task_id, benchmark=self.name, data=data)
                        tasks[task_id] = task

        return tasks

    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison."""
        # Basic normalization
        normalized = answer.strip()

        # Handle comma-separated lists
        if "," in normalized:
            # Split, strip whitespace, and rejoin
            parts = [p.strip() for p in normalized.split(",")]
            normalized = ", ".join(parts)

        # Handle numeric answers
        if self._is_numeric(normalized):
            # Remove unnecessary zeros and normalize format
            try:
                num = float(normalized)
                if num.is_integer():
                    normalized = str(int(num))
                else:
                    normalized = str(num)
            except ValueError:
                pass

        return normalized

    def _is_numeric(self, s: str) -> bool:
        """Check if string represents a number."""
        try:
            float(s.replace(",", ""))  # Handle numbers with commas
            return True
        except ValueError:
            return False

    def _check_partial_match(self, output: str, expected: str, task: Task) -> float:
        """Check for partial matches based on task type."""
        # For numeric answers, check if the number is close
        if self._is_numeric(expected) and self._is_numeric(output):
            try:
                expected_num = float(expected.replace(",", ""))
                output_num = float(output.replace(",", ""))
                # Allow 1% tolerance for numeric answers
                if abs(expected_num - output_num) / max(abs(expected_num), 1e-10) < 0.01:
                    return 0.9
            except ValueError:
                pass

        # For list answers, check if all elements are present
        if "," in expected and "," in output:
            expected_items = set(item.strip().lower() for item in expected.split(","))
            output_items = set(item.strip().lower() for item in output.split(","))
            if expected_items == output_items:
                return 0.9  # Full credit for correct items in different order
            elif expected_items.issubset(output_items) or output_items.issubset(expected_items):
                return 0.5  # Partial credit for subset matches

        # Case-insensitive match for certain types of answers
        if output.lower() == expected.lower():
            # Check if the task seems to require case-sensitive matching
            if task.data.get("Level", 1) >= 2:  # Higher level tasks might need exact match
                return 0.8
            else:
                return 0.9

        return 0.0

    def get_task_info(self, task_id: str) -> dict[str, Any]:
        """Get additional information about a task."""
        task = self.get_task(task_id)
        return {
            "question": task.data.get("Question", ""),
            "level": task.data.get("Level", None),
            "final_answer": task.data.get("Final answer", ""),
            "file_name": task.data.get("file_name", ""),
            "file_path": task.data.get("file_path", ""),
            "subset": task.data.get("subset", ""),
            "annotator_metadata": task.data.get("Annotator Metadata", {}),
        }

    def get_tasks_by_level(self, level: int) -> list[str]:
        """Get all task IDs for a specific difficulty level."""
        return [task_id for task_id, task in self._tasks.items() if task.data.get("Level") == level]

    def get_tasks_with_files(self) -> list[str]:
        """Get all task IDs that have associated files."""
        return [task_id for task_id, task in self._tasks.items() if task.data.get("file_name")]
