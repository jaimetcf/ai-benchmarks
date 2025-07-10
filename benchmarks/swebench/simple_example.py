#!/usr/bin/env python3
"""
Simple example: Evaluate a patch on a single SWEBench task using Modal.
"""

from benchmarks.benchmarks.swebench.swebench import SWEBenchVerified


def simple_modal_evaluation():
    """
    Demonstrates the core steps for SWEBench evaluation with Modal.
    """

    # 1. Initialize the benchmark
    benchmark = SWEBenchVerified()

    # 2. Get the first task for demonstration
    tasks = benchmark.get_tasks()
    task = tasks[0]  # Use first task as example

    print(f"Evaluating task: {task.task_id}")
    print(f"Task description: {task.data.get('problem_statement')}")
    print(f"Repository: {task.data.get('repo')}")
    print("=" * 80)

    # 3. Define a sample patch (this would normally come from your model)
    # Here, we're using the gold patch as the sample patch. This should always evaluate to True
    sample_patch = task.data.get("patch")

    if sample_patch is None:
        print("❌ No patch found for this task")
        return

    print("Sample patch preview (first 500 chars):")
    print(sample_patch[:500] + ("..." if len(sample_patch) > 500 else ""))
    print("=" * 80)

    # 4. Evaluate using Modal
    print("🚀 Starting Modal evaluation...")
    result = benchmark.evaluate_with_execution(task_id=task.task_id, output=sample_patch, use_modal=True)

    print(f"Evaluation result: {result}")

    # 5. You can also use the simple evaluate interface for compatibility
    print("\nUsing simple evaluate interface:")
    eval_result = benchmark.evaluate(task_id=task.task_id, output=sample_patch)
    print(f"Score: {eval_result.score}")
    print(f"Explanation: {eval_result.score_explanation}")


if __name__ == "__main__":
    simple_modal_evaluation()
