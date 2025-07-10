# AIME Benchmark

The AIME (American Invitational Mathematics Examination) benchmark tests mathematical problem-solving abilities on competition-level mathematics problems.

## Structure

The AIME benchmark consists of problems from the 2025 AIME competitions:
- **AIME 2025-I**: First exam (15 problems)
- **AIME 2025-II**: Second exam (15 problems)

Each problem requires an integer answer between 0 and 999.

## Data Format

Tasks are stored as individual JSON files in the `tasks/` directory with the following structure:
```json
{
  "task_id": "aime2025_aime2025_i_1",
  "question": "Problem statement",
  "evaluator_type": "aime",
  "source": "AIME2025",
  "domain": "mathematics",
  "level": null,
  "ground_truth": "70",
  "file_path": null,
  "metadata": {
    "subset": "AIME2025-I",
    "problem_number": 1
  },
  "evaluator_config": null
}
```

## Usage

```python
from benchmarks.AIME2025 import AIMEBenchmark

# Initialize the benchmark
benchmark = AIMEBenchmark()

# Get all task IDs
task_ids = benchmark.get_task_ids()

# Get a specific task
task = benchmark.get_task(task_id)

# Evaluate an answer
result = benchmark.evaluate(task_id, "42")
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")

# Get tasks by subset
aime_i_tasks = benchmark.get_tasks_by_subset("AIME2025-I")
aime_ii_tasks = benchmark.get_tasks_by_subset("AIME2025-II")

# Get problem numbers organized by subset
problem_numbers = benchmark.get_problem_numbers()
# Returns: {"AIME2025-I": [1, 2, ..., 15], "AIME2025-II": [1, 2, ..., 15]}

# Get detailed task information
task_info = benchmark.get_task_info(task_id)
# Returns: {
#   "question": "...",
#   "ground_truth": "70",
#   "source": "AIME2025",
#   "domain": "mathematics",
#   "subset": "AIME2025-I",
#   "problem_number": 1
# }
```

## Evaluation

The AIME benchmark uses exact match evaluation for integer answers:

1. **Exact Match (Score: 1.0)**: Answer matches the expected integer
2. **No Match (Score: 0.0)**: Answer doesn't match

The evaluator extracts numbers from the output text and checks if any match the expected answer. It handles:
- Simple integers: "42", "123"
- Decimals that equal integers: "42.0" → 42
- Fractions that equal integers: "84/2" → 42
- Numbers embedded in text: "The answer is 42"

## Answer Format

All AIME problems have integer answers in the range [0, 999]. The benchmark will:
- Extract all numbers from the output
- Normalize them (e.g., convert 42.0 to 42)
- Check if any match the expected answer

## Examples

```python
# Problem: Find the sum of all integer bases b>9 for which 17_b divides 97_b
result = benchmark.evaluate("aime2025_aime2025_i_1", "The sum is 70")
# Score: 1.0 (Correct!)

result = benchmark.evaluate("aime2025_aime2025_i_1", "70.0")
# Score: 1.0 (Correct! 70.0 is normalized to 70)

result = benchmark.evaluate("aime2025_aime2025_i_1", "140/2")
# Score: 1.0 (Correct! 140/2 = 70)
```

## Helper Methods

The benchmark provides several helper methods for working with the data:

- **`get_tasks_by_subset(subset)`**: Get all task IDs for a specific exam (AIME2025-I or AIME2025-II)
- **`get_problem_numbers()`**: Get a dictionary mapping subsets to their problem numbers
- **`get_task_info(task_id)`**: Get detailed information about a specific task

## Notes

- All answers are integers between 0 and 999
- The benchmark includes 30 problems total (15 from each exam)
- Problems test various mathematical topics including algebra, geometry, number theory, and combinatorics
- The evaluator is designed to be flexible in extracting numeric answers from text 