"""
Unified example demonstrating the common interface across all benchmarks.

This shows how AIME, GAIA, and SWE-bench all implement the same base interface,
allowing for consistent usage patterns.

Run this from the project root directory:
    python -m benchmarks.examples.unified_example
"""

from benchmarks.aime2025 import AIMEBenchmark
from benchmarks.gaia import GAIABenchmark
from benchmarks.swebench import SWEBenchVerified


def evaluate_on_benchmark(benchmark_class, model_output_func):
    """
    Generic function to evaluate on any benchmark using the common interface.

    Args:
        benchmark_class: The benchmark class to instantiate
        model_output_func: Function that takes a task and returns model output
    """
    # Initialize benchmark
    benchmark = benchmark_class()
    print(f"\n{'=' * 60}")
    print(f"Benchmark: {benchmark.name}")
    print(f"{'=' * 60}")

    # Get tasks
    task_ids = benchmark.get_task_ids()
    print(f"Total tasks: {len(task_ids)}")

    # Evaluate on first task
    if task_ids:
        task_id = task_ids[0]
        task = benchmark.get_task(task_id)

        print(f"\nTask ID: {task_id}")

        # Get model output for this task
        model_output = model_output_func(task)

        # Use the common evaluate interface
        result = benchmark.evaluate(task_id, model_output)

        print(f"Score: {result.score}")
        print(f"Explanation: {result.score_explanation}")

        # For execution-based benchmarks, we can also get detailed results
        if hasattr(benchmark, "evaluate_with_execution"):
            print("\nThis benchmark also supports detailed execution results.")


def main():
    """Demonstrate unified interface across all benchmarks."""

    print("Demonstrating unified benchmark interface")
    print("=" * 60)

    # AIME: Math problems with integer answers
    def aime_model(task):
        # A real model would solve the math problem
        # This just returns a dummy answer
        return "42"

    evaluate_on_benchmark(AIMEBenchmark, aime_model)

    # GAIA: General assistant tasks
    def gaia_model(task):
        # A real model would analyze the question and potentially use tools
        # This just returns a simple answer
        question = task.data.get("Question", "").lower()
        if "how many" in question:
            return "10"
        elif "what year" in question:
            return "2023"
        else:
            return "Paris"

    evaluate_on_benchmark(GAIABenchmark, gaia_model)

    # SWE-bench: Code patches
    def swebench_model(task):
        # A real model would generate a patch to fix the issue
        # This returns a dummy patch
        return """--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,3 @@
 def hello():
-    return "Hello"
+    return "Hello, World!"
"""

    # Note: SWE-bench evaluation requires Docker/Modal setup
    print("\n" + "=" * 60)
    print("SWE-bench example (requires Docker/Modal):")
    print("=" * 60)
    try:
        evaluate_on_benchmark(SWEBenchVerified, swebench_model)
    except Exception as e:
        print(f"SWE-bench evaluation skipped: {e}")
        print("(This is expected if Docker/Modal is not set up)")


if __name__ == "__main__":
    main()
