"""
Example script demonstrating how to use the GAIA benchmark.

This shows the basic pattern for evaluating a model on the benchmark.

Run this from the project root directory:
    python -m benchmarks.example_gaia
"""

from benchmarks.gaia import GAIABenchmark


class TrivialAssistantModel:
    """A trivial model that gives simple answers based on keywords."""

    def __init__(self):
        self.name = "TrivialAssistant"

    def answer(self, question: str) -> str:
        """
        'Answer' a question by looking for keywords.
        In a real model, this would use tools, search, reasoning, etc.
        """
        # A real model would use various tools and reasoning here
        question_lower = question.lower()

        if "how many" in question_lower:
            return "42"
        elif "what year" in question_lower or "when was" in question_lower:
            return "2023"
        elif "which" in question_lower or "who" in question_lower:
            return "Paris"
        elif "population" in question_lower:
            return "1000000"
        else:
            return "I don't know"


def evaluate_model_on_gaia():
    """Demonstrate evaluating a model on the GAIA benchmark."""

    # Initialize the benchmark
    benchmark = GAIABenchmark()

    # Initialize our "model"
    model = TrivialAssistantModel()

    print(f"Evaluating {model.name} on {benchmark.name} benchmark")
    print("=" * 60)

    # Get some Level 1 tasks (easier ones) for demo
    level_1_tasks = benchmark.get_tasks_by_level(1)[:5]

    total_score = 0
    results = []

    for task_id in level_1_tasks:
        # Get the task
        task = benchmark.get_task(task_id)

        # Get task info
        task_info = benchmark.get_task_info(task_id)
        question = task_info["question"]
        expected = task_info["final_answer"]

        # Run the model
        model_output = model.answer(question)

        # Evaluate the output
        result = benchmark.evaluate(task_id, model_output)

        # Store results
        total_score += result.score
        results.append({"task_id": task_id, "score": result.score, "explanation": result.score_explanation, "model_output": model_output})

        # Print individual result
        print(f"\nTask: {task_id}")
        print(f"Question: {question[:80]}...")
        print(f"Expected: {expected}")
        print(f"Model output: {model_output}")
        print(f"Score: {result.score}")
        print(f"Explanation: {result.score_explanation}")

    # Calculate and print summary statistics
    accuracy = total_score / len(level_1_tasks) if level_1_tasks else 0
    print("\n" + "=" * 60)
    print(f"Summary: {total_score}/{len(level_1_tasks)} correct ({accuracy:.1%} accuracy)")

    # Demonstrate using helper methods
    print("\n" + "=" * 60)
    print("Additional benchmark information:")

    # Show task distribution by level
    for level in [1, 2, 3]:
        level_tasks = benchmark.get_tasks_by_level(level)
        print(f"- Level {level}: {len(level_tasks)} tasks")

    # Show tasks with files
    tasks_with_files = benchmark.get_tasks_with_files()
    print(f"- Tasks with associated files: {len(tasks_with_files)}")

    # Show an example of a task with a file
    if tasks_with_files:
        example_file_task = tasks_with_files[0]
        file_info = benchmark.get_task_info(example_file_task)
        print("\nExample task with file:")
        print(f"  Task ID: {example_file_task}")
        print(f"  File: {file_info['file_name']}")
        print(f"  Question: {file_info['question'][:60]}...")

    return results


def main():
    """Run the example evaluation."""
    results = evaluate_model_on_gaia()

    # You could save results to a file, send to a database, etc.
    print("\nEvaluation complete!")
    print("\nNote: GAIA tasks often require web search, file analysis, and multi-step reasoning.")
    print("A real model would need to implement these capabilities.")


if __name__ == "__main__":
    main()
