"""
BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents
Authors: Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jeffrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, Mia Glaese
https://openai.com/index/browsecomp/
"""

import base64
import hashlib
import re
from pathlib import Path
from typing import Any

import pandas as pd

from benchmarks.core.base_benchmark import BaseBenchmark
from benchmarks.core.models.task import EvaluationResult, Task


class BrowseCompBenchmark(BaseBenchmark):
    """
    BrowseComp is a benchmark for evaluating browsing agents.

    The benchmark consists of tasks that require browsing the web to find answers.
    Questions and answers are encrypted in the dataset for security.
    """

    # Query template for formatting questions
    QUERY_TEMPLATE = """
{Question}

Your response should be in the following format:
Explanation: {{your explanation for your final answer}}
Exact Answer: {{your succinct, final answer}}
Confidence: {{your confidence score between 0% and 100% for your answer}}
""".strip()

    def __init__(self, data_dir: str | None = None):
        """Initialize the BrowseComp benchmark.

        Args:
            data_dir: Optional path to data directory. If None, downloads from OpenAI's public dataset.
        """
        self.data_dir = Path(data_dir) if data_dir else None
        self._tasks = self._load_tasks()

    @property
    def name(self) -> str:
        """Return the benchmark name."""
        return "BrowseComp"

    def get_task_ids(self) -> list[str]:
        """Return all task IDs."""
        return list(self._tasks.keys())

    def get_task(self, task_id: str) -> Task:
        """Get a specific task by ID."""
        if task_id not in self._tasks:
            raise ValueError(f"Task {task_id} not found")
        return self._tasks[task_id]

    def evaluate(self, task_id: str, output: Any) -> EvaluationResult:
        """Evaluate the model output for a task.

        Args:
            task_id: The task ID to evaluate
            output: The model's output

        Returns:
            EvaluationResult with score and explanation
        """
        task = self.get_task(task_id)
        correct_answer = task.data["answer"]

        # Simple evaluation: check if the answer is correct
        # For more sophisticated evaluation, you might want to use a grader model
        score = self._simple_grade(output, correct_answer)

        if score > 0.5:
            return EvaluationResult(score=1.0, score_explanation="Correct answer provided")
        else:
            return EvaluationResult(score=0.0, score_explanation=f"Incorrect. Expected answer related to: {correct_answer[:50]}...")

    def _load_tasks(self) -> dict[str, Task]:
        """Load tasks from the BrowseComp dataset."""
        # Load the CSV from OpenAI's public dataset
        df = pd.read_csv("https://openaipublic.blob.core.windows.net/simple-evals/browse_comp_test_set.csv")

        tasks = {}
        for idx, row in df.iterrows():
            # Decrypt the problem and answer
            problem = self._decrypt(row.get("problem", ""), row.get("canary", ""))
            answer = self._decrypt(row.get("answer", ""), row.get("canary", ""))

            # Create task ID
            task_id = f"browsecomp_{idx:04d}"

            # Create task data
            task_data = {
                "task_id": task_id,
                "question": problem,
                "answer": answer,
                "canary": row.get("canary", ""),
                "index": idx,
            }

            # Create Task object
            task = Task(task_id=task_id, benchmark=self.name, data=task_data)

            tasks[task_id] = task

        return tasks

    def _derive_key(self, password: str, length: int) -> bytes:
        """Derive a fixed-length key from the password using SHA256."""
        hasher = hashlib.sha256()
        hasher.update(password.encode())
        key = hasher.digest()
        return key * (length // len(key)) + key[: length % len(key)]

    def _decrypt(self, ciphertext_b64: str, password: str) -> str:
        """Decrypt base64-encoded ciphertext with XOR."""
        if not ciphertext_b64 or not password:
            return ""

        try:
            encrypted = base64.b64decode(ciphertext_b64)
            key = self._derive_key(password, len(encrypted))
            decrypted = bytes(a ^ b for a, b in zip(encrypted, key, strict=False))
            return decrypted.decode()
        except Exception:
            return ""

    def _simple_grade(self, response: Any, correct_answer: str) -> float:
        """Simple grading function that checks if key parts of the answer are present."""
        if response is None:
            return 0.0

        response_str = str(response).lower()
        correct_answer_lower = correct_answer.lower()

        # Extract the final answer from the response if it follows the template
        final_answer_match = re.search(r"exact answer:\s*(.+?)(?:\n|$)", response_str, re.IGNORECASE)
        if final_answer_match:
            final_answer = final_answer_match.group(1).strip()
            # Check for exact match (case-insensitive)
            if final_answer == correct_answer_lower:
                return 1.0
            # Check if the correct answer is contained in the final answer
            if correct_answer_lower in final_answer:
                return 0.8

        # Fallback: check if correct answer appears anywhere in response
        if correct_answer_lower in response_str:
            return 0.6

        return 0.0

    def get_task_info(self, task_id: str) -> dict[str, Any]:
        """Get additional information about a task."""
        task = self.get_task(task_id)
        return {
            "question": task.data.get("question", ""),
            "answer": task.data.get("answer", ""),
            "index": task.data.get("index", None),
        }

    def format_question(self, task_id: str) -> str:
        """Format a question using the standard template."""
        task = self.get_task(task_id)
        return self.QUERY_TEMPLATE.format(Question=task.data["question"])
