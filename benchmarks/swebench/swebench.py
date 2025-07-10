import json
import time
from typing import Any, cast

from datasets import load_dataset

import docker
from benchmarks.benchmarks.swebench.harness.constants import KEY_INSTANCE_ID, KEY_MODEL, KEY_PREDICTION, SWEbenchInstance
from benchmarks.benchmarks.swebench.harness.modal_eval import run_instances_modal
from benchmarks.benchmarks.swebench.harness.run_evaluation import run_instance
from benchmarks.benchmarks.swebench.harness.test_spec.test_spec import make_test_spec
from benchmarks.core.base_benchmark import CodeExecutionBenchmark
from benchmarks.core.models.task import EvaluationResult, ExecutionResult, Task, TaskResult

# Login using e.g. `huggingface-cli login` to access this dataset


class SWEBenchVerified(CodeExecutionBenchmark):
    def __init__(self):
        # Load dataset without streaming to get proper Dataset object
        self.ds = load_dataset("princeton-nlp/SWE-bench_Verified", streaming=False)
        self._test_data: list[dict[str, Any]] | None = None

    @property
    def name(self) -> str:
        """Benchmark name."""
        return "SWE-bench_Verified"

    @property
    def task_structure(self) -> dict[str, Any]:
        """Dataset structure."""
        # DatasetDict doesn't have features directly, access from the test split
        return {
            "repo": "Repository owner/name identifier",
            "instance_id": "Formatted instance identifier (repo_owner__repo_name-PR-number)",
            "base_commit": "Commit hash before the solution PR is applied",
            "patch": "Gold patch that resolved the issue (excluding test code)",
            "test_patch": "Test-file patch contributed by the solution PR",
            "problem_statement": "Issue title and body (the actual problem to solve)",
            "hints_text": "Comments made on the issue prior to solution",
            "created_at": "Creation date of the pull request",
            "version": "Installation version for evaluation",
            "environment_setup_commit": "Commit hash to use for environment setup and installation",
            "FAIL_TO_PASS": "Tests that should pass after applying the fix",
            "PASS_TO_PASS": "Tests that should pass before and after the fix",
        }

    @property
    def task_inputs(self) -> dict[str, Any]:
        # The inputs to the task contains the full task structure excluding the test_patch, the patch (gold patch), and certain metadata
        task_inputs = self.task_structure
        task_inputs.pop("test_patch")
        task_inputs.pop("patch")
        task_inputs.pop("difficulty") if "difficulty" in task_inputs else None
        return task_inputs

    def _get_test_data(self) -> list[dict[str, Any]]:
        """Cache and return the test data."""
        if self._test_data is None:
            # Convert to proper type - we know these are dicts
            self._test_data = [dict(item) for item in self.ds["test"]]  # type: ignore
        return self._test_data

    def get_task_ids(self) -> list[str]:
        """Get all task IDs for this benchmark."""
        return [task.task_id for task in self.get_tasks()]

    def get_task(self, task_id: str) -> Task:
        """Get a task object by its ID."""
        task = next((task for task in self.get_tasks() if task.task_id == task_id), None)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found")
        return task

    def get_tasks(self) -> list[Task]:
        """Get all tasks for this benchmark."""
        tasks = []
        test_data = self._get_test_data()

        for example in test_data:
            # Convert FAIL_TO_PASS and PASS_TO_PASS from strings to lists if needed
            for key in ["FAIL_TO_PASS", "PASS_TO_PASS"]:
                if key in example and isinstance(example[key], str):
                    try:
                        example[key] = json.loads(example[key])
                    except json.JSONDecodeError:
                        example[key] = []

            # Store all SWE-bench data directly in the task data field
            task = Task(
                task_id=example["instance_id"],
                benchmark=self.name,
                data=example,  # Store the entire example data structure
            )
            tasks.append(task)

        return tasks

    def evaluate_with_execution(self, task_id: str, output: Any, **kwargs) -> TaskResult:
        """
        Evaluate code (patch) on a SWE-bench task using the official harness.

        Args:
            task_id: The task ID to evaluate
            output: The generated patch/code to evaluate
            **kwargs: Additional parameters:
                - use_modal (bool): If True, use Modal for cloud execution instead of local Docker

        Returns:
            TaskResult with evaluation results
        """
        task = self.get_task(task_id)
        use_modal = kwargs.get("use_modal", True)

        start_time = time.time()

        try:
            if use_modal:
                return self._evaluate_with_modal(output, task, start_time)
            else:
                return self._evaluate_with_docker(output, task, start_time)

        except Exception as e:
            execution_time = time.time() - start_time
            return TaskResult(
                task_id=task.task_id,
                benchmark_name=self.name,
                execution=ExecutionResult(
                    execution_output=None,
                    execution_trace=f"Exception during evaluation: {e!s}",
                    error=str(e),
                    execution_time=execution_time,
                ),
                evaluation=None,
            )

    def _evaluate_with_modal(self, code: str, task: Task, start_time: float) -> TaskResult:
        """Evaluate using Modal cloud execution."""

        # Create prediction dict
        prediction = {
            KEY_INSTANCE_ID: task.task_id,
            KEY_MODEL: "swe_bench_evaluator",
            KEY_PREDICTION: code,
        }
        predictions = {task.task_id: prediction}

        # Create dataset entry from task
        dataset = [task.data]
        full_dataset = dataset

        run_id = f"modal_eval_{task.task_id}_{int(time.time())}"
        timeout = 1800

        # Run on Modal - this returns a Path to the report file
        report_path = run_instances_modal(predictions, dataset, full_dataset, run_id, timeout)

        execution_time = time.time() - start_time

        # Try to read the report to get results
        try:
            if report_path and report_path.exists():
                with open(report_path) as f:
                    report_data = json.load(f)

                # Check if the task was resolved
                resolved = task.task_id in report_data.get("resolved_ids", [])
                score = 1.0 if resolved else 0.0

                return TaskResult(
                    task_id=task.task_id,
                    benchmark_name=self.name,
                    execution=ExecutionResult(
                        execution_output=report_data,
                        execution_trace=json.dumps({"report_path": str(report_path), "resolved": resolved, "execution_method": "modal"}, indent=2),
                        error=None,
                        execution_time=execution_time,
                    ),
                    evaluation=EvaluationResult(
                        score=score,
                        score_explanation=f"Task resolved: {resolved}",
                    ),
                )
            else:
                # No report file found
                return TaskResult(
                    task_id=task.task_id,
                    benchmark_name=self.name,
                    execution=ExecutionResult(
                        execution_output=None,
                        execution_trace="No report file generated",
                        error="Modal evaluation did not produce a report",
                        execution_time=execution_time,
                    ),
                    evaluation=None,
                )
        except Exception as e:
            return TaskResult(
                task_id=task.task_id,
                benchmark_name=self.name,
                execution=ExecutionResult(
                    execution_output=None,
                    execution_trace=f"Error reading report: {e!s}",
                    error=str(e),
                    execution_time=execution_time,
                ),
                evaluation=None,
            )

    def _evaluate_with_docker(self, code: str, task: Task, start_time: float) -> TaskResult:
        """Evaluate using local Docker execution."""
        # The task data already contains all the SWE-bench instance data
        # Cast to the expected type for the harness

        test_spec = make_test_spec(cast(SWEbenchInstance, task.data))

        # Create prediction dict
        prediction = {
            KEY_INSTANCE_ID: task.task_id,
            KEY_MODEL: "swe_bench_evaluator",
            KEY_PREDICTION: code,  # The generated patch
        }

        # Setup Docker client and evaluation parameters
        client = docker.from_env()
        run_id = f"eval_{task.task_id}_{int(time.time())}"
        timeout = 1800  # 30 minutes timeout

        # Run the evaluation instance
        result = run_instance(
            test_spec=test_spec,
            pred=prediction,
            rm_image=True,  # Clean up images after evaluation
            force_rebuild=False,
            client=client,
            run_id=run_id,
            timeout=timeout,
            rewrite_reports=False,
        )

        execution_time = time.time() - start_time

        if result is None:
            # Evaluation failed
            return TaskResult(
                task_id=task.task_id,
                benchmark_name=self.name,
                execution=ExecutionResult(
                    execution_output=None,
                    execution_trace="Evaluation failed - no result returned",
                    error="Evaluation harness returned None",
                    execution_time=execution_time,
                ),
                evaluation=None,
            )

        instance_id, report = result

        # Extract score from report
        instance_report = report.get(instance_id, {})
        resolved = instance_report.get("resolved", False)
        score = 1.0 if resolved else 0.0

        # Create execution trace from report
        trace_info = {
            "patch_applied": instance_report.get("patch_successfully_applied", False),
            "patch_exists": instance_report.get("patch_exists", False),
            "resolved": resolved,
            "tests_status": instance_report.get("tests_status", {}),
            "execution_method": "docker",
        }

        return TaskResult(
            task_id=task.task_id,
            benchmark_name=self.name,
            execution=ExecutionResult(
                execution_output=report,
                execution_trace=json.dumps(trace_info, indent=2),
                error=None,
                execution_time=execution_time,
            ),
            evaluation=EvaluationResult(
                score=score,
                score_explanation=f"Patch applied: {trace_info['patch_applied']}, Task resolved: {trace_info['resolved']}",
            ),
        )

    def score(self, output: Any, expected: Any) -> float:
        # TODO: Implement proper scoring logic for SWE-bench
        # This should compare generated patches/solutions with expected patches
        # For now, return a placeholder score
        return 0.0


if __name__ == "__main__":
    # Example usage
    benchmark = SWEBenchVerified()
    print(f"Benchmark: {benchmark.name}")
    print(f"Task structure: {benchmark.task_structure}")

    tasks = benchmark.get_tasks()
    if tasks:
        task = tasks[0]
        print("\nFirst task:")
        print(f"Task ID: {task.task_id}")
        print(f"Benchmark: {task.benchmark}")
        print(f"Data keys: {list(task.data.keys())}")
        print(f"Repository: {task.data.get('repo', 'N/A')}")
        print(f"Problem statement length: {len(task.data.get('problem_statement', ''))}")
        print(f"Gold patch length: {len(task.data.get('patch', ''))}")
