"""Test script for AIME benchmark implementation."""

from benchmarks.aime2025 import AIMEBenchmark


def test_aime_benchmark():
    # Initialize the benchmark
    benchmark = AIMEBenchmark()

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
        print(f"Question: {task.data.get('question', 'N/A')[:100]}...")
        print(f"Expected answer: {task.data.get('ground_truth', 'N/A')}")
        print(f"Source: {task.data.get('source', 'N/A')}")
        print(f"Domain: {task.data.get('domain', 'N/A')}")

        # Test evaluation with different types of answers
        test_outputs = [
            task.data.get("ground_truth", ""),  # Correct answer
            "999",  # Wrong answer
            f" {task.data.get('ground_truth', '')} ",  # Correct with whitespace
            "42",  # Another wrong answer
            f"{task.data.get('ground_truth', '')}.0",  # Correct as decimal
        ]

        print("\nTesting evaluation:")
        for output in test_outputs:
            result = benchmark.evaluate(first_task_id, output)
            print(f"Output: '{output}' -> Score: {result.score}, Explanation: {result.score_explanation}")

        # Show a few examples of different problems
        print("\nExample AIME problems:")
        for i, task_id in enumerate(task_ids[:5]):
            task = benchmark.get_task(task_id)
            metadata = task.data.get("metadata", {})
            print(f"\n{i + 1}. Task {task_id}:")
            print(f"   Question: {task.data.get('question', '')[:80]}...")
            print(f"   Answer: {task.data.get('ground_truth', '')}")
            print(f"   Subset: {metadata.get('subset', 'N/A')}")
            print(f"   Problem #: {metadata.get('problem_number', 'N/A')}")

        # Test the number extraction functionality
        print("\nTesting number extraction:")
        test_strings = [
            "The answer is 42",
            "42 is the answer",
            "I got 3/4 as my result",
            "The value is 3.14159",
            "No numbers here!",
            "Multiple: 10, 20, 30",
        ]
        for test_str in test_strings:
            # Access the private method for testing
            numbers = benchmark._extract_numbers(test_str)
            print(f"'{test_str}' -> {numbers}")

        # Test new helper methods
        print("\nTesting helper methods:")

        # Test get_tasks_by_subset
        aime_i_tasks = benchmark.get_tasks_by_subset("AIME2025-I")
        aime_ii_tasks = benchmark.get_tasks_by_subset("AIME2025-II")
        print("\nTasks by subset:")
        print(f"  AIME2025-I: {len(aime_i_tasks)} tasks")
        print(f"  AIME2025-II: {len(aime_ii_tasks)} tasks")

        # Test get_problem_numbers
        problem_numbers = benchmark.get_problem_numbers()
        print("\nProblem numbers by subset:")
        for subset, numbers in problem_numbers.items():
            print(f"  {subset}: {numbers}")

        # Test get_task_info
        print(f"\nDetailed task info for {first_task_id}:")
        task_info = benchmark.get_task_info(first_task_id)
        for key, value in task_info.items():
            if key == "question" and len(str(value)) > 80:
                print(f"  {key}: {str(value)[:80]}...")
            else:
                print(f"  {key}: {value}")


if __name__ == "__main__":
    test_aime_benchmark()
