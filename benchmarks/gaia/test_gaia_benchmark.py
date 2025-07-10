"""Test script for GAIA benchmark implementation."""

from benchmarks.gaia import GAIABenchmark


def test_gaia_benchmark():
    # Initialize the benchmark
    benchmark = GAIABenchmark()

    print(f"Benchmark name: {benchmark.name}")

    # Get all task IDs
    task_ids = benchmark.get_task_ids()
    print(f"Total number of tasks: {len(task_ids)}")

    # Test with a few tasks
    if task_ids:
        # Get first task
        first_task_id = task_ids[0]
        task = benchmark.get_task(first_task_id)

        print(f"\nFirst task ID: {first_task_id}")
        print(f"Question: {task.data.get('Question', 'N/A')[:100]}...")
        print(f"Expected answer: {task.data.get('Final answer', 'N/A')}")
        print(f"Level: {task.data.get('Level', 'N/A')}")
        print(f"Has file: {'Yes' if task.data.get('file_name') else 'No'}")

        # Test evaluation
        test_outputs = [
            task.data.get("Final answer", ""),  # Correct answer
            "wrong answer",  # Wrong answer
            task.data.get("Final answer", "").upper() if isinstance(task.data.get("Final answer", ""), str) else "WRONG",  # Case variation
        ]

        print("\nTesting evaluation:")
        for output in test_outputs:
            result = benchmark.evaluate(first_task_id, output)
            print(f"Output: '{output}' -> Score: {result.score}, Explanation: {result.score_explanation}")

        # Test helper methods
        print("\nTasks by level:")
        for level in [1, 2, 3]:
            level_tasks = benchmark.get_tasks_by_level(level)
            print(f"  Level {level}: {len(level_tasks)} tasks")

        tasks_with_files = benchmark.get_tasks_with_files()
        print(f"\nTasks with files: {len(tasks_with_files)}")

        # Show a few examples of different answer types
        print("\nExample tasks with different answer types:")
        for i, task_id in enumerate(task_ids[:5]):
            task_info = benchmark.get_task_info(task_id)
            print(f"\n{i + 1}. Task {task_id}:")
            print(f"   Question: {task_info['question'][:80]}...")
            print(f"   Answer: {task_info['final_answer']}")
            print(f"   Level: {task_info['level']}")


if __name__ == "__main__":
    test_gaia_benchmark()
