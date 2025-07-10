# GAIA Benchmark

The GAIA (General AI Assistants) benchmark is designed to test AI systems on real-world tasks that require various capabilities including web search, file handling, multi-step reasoning, and tool use.

## Structure

The GAIA benchmark consists of questions at three difficulty levels:
- **Level 1**: Simple tasks requiring basic reasoning
- **Level 2**: Intermediate tasks requiring multiple steps or file analysis
- **Level 3**: Complex tasks requiring extensive research and reasoning

## Data Format

Tasks are stored in `metadata.jsonl` files with the following structure:
```json
{
  "task_id": "unique-identifier",
  "Question": "The question text",
  "Level": 1-3,
  "Final answer": "Expected answer",
  "file_name": "associated_file.ext",  // Optional
  "Annotator Metadata": {
    "Steps": "Human annotator's solution steps",
    "Number of steps": "N",
    "How long did this take?": "Time estimate",
    "Tools": "List of tools used",
    "Number of tools": "N"
  }
}
```

## Usage

```python
from benchmarks.GAIA import GAIABenchmark

# Initialize the benchmark
benchmark = GAIABenchmark()

# Get all task IDs
task_ids = benchmark.get_task_ids()

# Get a specific task
task = benchmark.get_task(task_id)

# Evaluate an answer
result = benchmark.evaluate(task_id, "your answer")
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")

# Get tasks by difficulty level
level_2_tasks = benchmark.get_tasks_by_level(2)

# Get tasks that have associated files
tasks_with_files = benchmark.get_tasks_with_files()
```

## Evaluation

The GAIA benchmark uses exact match evaluation with some normalization:

1. **Exact Match (Score: 1.0)**: Answer exactly matches the expected answer
2. **Normalized Match (Score: 0.9-1.0)**: 
   - Case-insensitive matches for Level 1 tasks
   - Numeric answers within 1% tolerance
   - List answers with correct items in different order
3. **Partial Match (Score: 0.5-0.8)**: Subset matches for list answers
4. **No Match (Score: 0.0)**: Answer doesn't match expected

## File Support

Many GAIA tasks include associated files such as:
- Spreadsheets (.xlsx, .csv)
- Documents (.pdf, .docx, .txt)
- Images (.png, .jpg)
- Audio files (.mp3, .m4a)
- Code files (.py, .json, .xml)
- And more...

The benchmark automatically tracks file paths for tasks with associated files.

## Notes

- The benchmark includes both validation and test sets
- Answers are case-sensitive by default (except for Level 1 tasks)
- Some answers may be numeric, lists, or single words/phrases
- The evaluation includes smart normalization for common answer formats 