"""
Example script demonstrating how to use the AIME benchmark.

This shows the basic pattern for evaluating a model on the benchmark.

Run this from the project root directory:
    python -m benchmarks.example
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from benchmarks.aime2025 import AIMEBenchmark


class TrivialMathModel:
    """A trivial model that always returns a random answer between 0-999."""

    def __init__(self):
        self.name = "TrivialMathModel"

    def solve(self, problem: str) -> str:
        """
        'Solve' a math problem by returning a random answer.
        In a real model, this would actually process the problem text.
        """
        # A real model would analyze the problem here
        # For demo purposes, we'll just return different fixed answers
        if "bases" in problem.lower():
            return "The answer is 70"
        elif "circle" in problem.lower():
            return "I calculated 293"
        elif "divisors" in problem.lower():
            return "237"
        else:
            return "42"  # Default answer


def evaluate_model_on_aime():
    """Demonstrate evaluating a model on the AIME benchmark."""

    # Initialize the benchmark
    benchmark = AIMEBenchmark()

    # Initialize our "model"
    model = TrivialMathModel()

    print(f"Evaluating {model.name} on {benchmark.name} benchmark")
    print("=" * 60)

    # Get all task IDs (or you could use a subset)
    task_ids = benchmark.get_task_ids()

    # For demo, let's just evaluate on the first 5 problems
    demo_task_ids = task_ids[:5]

    total_score = 0
    results = []

    for task_id in demo_task_ids:
        # Get the task
        task = benchmark.get_task(task_id)

        # Get the problem text
        problem = task.data["question"]

        # Run the model
        model_output = model.solve(problem)

        # Evaluate the output
        result = benchmark.evaluate(task_id, model_output)

        # Store results
        total_score += result.score
        results.append({"task_id": task_id, "score": result.score, "explanation": result.score_explanation, "model_output": model_output})

        # Print individual result
        print(f"\nTask: {task_id}")
        print(f"Problem: {problem[:80]}...")
        print(f"Model output: {model_output}")
        print(f"Score: {result.score}")
        print(f"Explanation: {result.score_explanation}")

    # Calculate and print summary statistics
    accuracy = total_score / len(demo_task_ids)
    print("\n" + "=" * 60)
    print(f"Summary: {total_score}/{len(demo_task_ids)} correct ({accuracy:.1%} accuracy)")

    # Demonstrate using helper methods
    print("\n" + "=" * 60)
    print("Additional benchmark information:")

    # Show tasks by subset
    aime_i_tasks = benchmark.get_tasks_by_subset("AIME2025-I")
    aime_ii_tasks = benchmark.get_tasks_by_subset("AIME2025-II")
    print(f"- AIME 2025-I has {len(aime_i_tasks)} problems")
    print(f"- AIME 2025-II has {len(aime_ii_tasks)} problems")

    # Show problem numbers
    problem_numbers = benchmark.get_problem_numbers()
    print(f"- Problem numbers available: {list(problem_numbers.keys())}")

    return results


def main():
    """Run the example evaluation."""
    results = evaluate_model_on_aime()

    # You could save results to a file, send to a database, etc.
    print("\nEvaluation complete!")


if __name__ == "__main__":
    main()
