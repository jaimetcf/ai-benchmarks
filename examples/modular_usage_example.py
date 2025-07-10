#!/usr/bin/env python3
"""
Example demonstrating modular usage of benchmarks.

This example shows how to use benchmarks selectively based on what's installed.
"""

# Core components are always available when the base package is installed
from core import BaseBenchmark, Task, EvaluationResult


def run_benchmark_if_available(benchmark_name: str):
    """Try to run a specific benchmark if it's installed."""

    if benchmark_name == "aime":
        try:
            from benchmarks.aime2025 import AIMEBenchmark

            print("✓ AIME benchmark is installed")

            # Create benchmark instance
            benchmark = AIMEBenchmark()

            # Get first task
            task_ids = benchmark.get_task_ids()
            if task_ids:
                task_id = task_ids[0]
                task = benchmark.get_task(task_id)

                print(f"  Task ID: {task_id}")
                print(f"  Question: {task.data.get('question', '')[:100]}...")

                # Example evaluation
                result = benchmark.evaluate(task_id, "123")
                print(f"  Score: {result.score}")

        except ImportError:
            print("✗ AIME benchmark not installed")
            print("  Install with: uv pip install -e '.[aime]'")

    elif benchmark_name == "gaia":
        try:
            from benchmarks.gaia import GAIABenchmark

            print("✓ GAIA benchmark is installed")

            # Create benchmark instance
            benchmark = GAIABenchmark()

            # Get first task
            task_ids = benchmark.get_task_ids()
            if task_ids:
                task_id = task_ids[0]
                task = benchmark.get_task(task_id)

                print(f"  Task ID: {task_id}")
                print(f"  Question: {task.data.get('Question', '')[:100]}...")

        except ImportError:
            print("✗ GAIA benchmark not installed")
            print("  Install with: uv pip install -e '.[gaia]'")

    elif benchmark_name == "swebench":
        try:
            from benchmarks.swebench import SWEBenchVerified

            print("✓ SWE-bench benchmark is installed")

            # Note: SWE-bench requires additional setup (Docker, etc.)
            benchmark = SWEBenchVerified()
            print(f"  Number of tasks: {len(benchmark.get_task_ids())}")

        except ImportError:
            print("✗ SWE-bench benchmark not installed")
            print("  Install with: uv pip install -e '.[swebench]'")
            print("  Note: SWE-bench requires Docker and other dependencies")


def main():
    """Check which benchmarks are available."""
    print("AI Benchmarks - Modular Usage Example")
    print("=====================================\n")

    print("Checking installed benchmarks...\n")

    # Check each benchmark
    for benchmark in ["aime", "gaia", "swebench"]:
        run_benchmark_if_available(benchmark)
        print()

    print("\nTo install all benchmarks:")
    print("  uv pip install -e '.[all]'")

    print("\nTo install specific benchmarks:")
    print("  uv pip install -e '.[aime]'")
    print("  uv pip install -e '.[gaia]'")
    print("  uv pip install -e '.[swebench]'")


if __name__ == "__main__":
    main()
