"""Example usage of BrowseComp benchmark."""

from benchmarks.browse_comp import BrowseCompBenchmark


def main():
    # Initialize benchmark
    print("Loading BrowseComp benchmark...")
    benchmark = BrowseCompBenchmark()

    # Get task information
    task_ids = benchmark.get_task_ids()
    print(f"Total tasks: {len(task_ids)}")

    # Example with first few tasks
    for i, task_id in enumerate(task_ids[:3]):
        print(f"\n{'=' * 60}")
        print(f"Task {i + 1}: {task_id}")
        print(f"{'=' * 60}")

        # Get task details
        task = benchmark.get_task(task_id)
        task_info = benchmark.get_task_info(task_id)

        # Display question using the standard template
        formatted_question = benchmark.format_question(task_id)
        print(f"\nFormatted Question:")
        print(formatted_question)

        # Show the raw question and answer (for demonstration)
        print(f"\nRaw Question: {task_info['question'][:200]}..." if len(task_info["question"]) > 200 else f"\nRaw Question: {task_info['question']}")
        print(f"Answer Preview: {task_info['answer'][:50]}..." if len(task_info["answer"]) > 50 else f"Answer: {task_info['answer']}")

        # Example evaluation with different response formats
        print("\n--- Example Evaluations ---")

        # Example 1: Properly formatted response
        model_output_1 = f"""
Explanation: Based on my analysis of the question, I have determined the answer.
Exact Answer: {task_info["answer"]}
Confidence: 95%
"""
        result_1 = benchmark.evaluate(task_id, model_output_1)
        print(f"\nExample 1 (Properly formatted):")
        print(f"Score: {result_1.score}")
        print(f"Explanation: {result_1.score_explanation}")

        # Example 2: Answer embedded in text
        model_output_2 = f"I think the answer is {task_info['answer']} based on my research."
        result_2 = benchmark.evaluate(task_id, model_output_2)
        print(f"\nExample 2 (Answer in text):")
        print(f"Score: {result_2.score}")
        print(f"Explanation: {result_2.score_explanation}")

        # Example 3: Wrong answer
        model_output_3 = "The answer is definitely 42."
        result_3 = benchmark.evaluate(task_id, model_output_3)
        print(f"\nExample 3 (Wrong answer):")
        print(f"Score: {result_3.score}")
        print(f"Explanation: {result_3.score_explanation}")

    # Show statistics
    print(f"\n{'=' * 60}")
    print("Benchmark Statistics:")
    print(f"{'=' * 60}")
    print(f"Total number of tasks: {len(task_ids)}")
    print(f"Task ID format: {task_ids[0] if task_ids else 'N/A'}")

    # Demonstrate batch evaluation
    print("\n--- Batch Evaluation Example ---")
    sample_size = min(5, len(task_ids))
    total_score = 0

    for task_id in task_ids[:sample_size]:
        task_info = benchmark.get_task_info(task_id)
        # Simulate a model that gets 60% correct
        import random

        if random.random() < 0.6:
            output = f"Exact Answer: {task_info['answer']}"
        else:
            output = "Exact Answer: incorrect answer"

        result = benchmark.evaluate(task_id, output)
        total_score += result.score

    print(f"Average score over {sample_size} tasks: {total_score / sample_size:.2f}")


if __name__ == "__main__":
    main()
