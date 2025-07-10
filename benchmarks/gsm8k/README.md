# GSM8K Benchmark

The GSM8K (Grade School Math 8K) benchmark tests mathematical reasoning abilities on grade school word problems.

## Structure

The GSM8K benchmark consists of grade school math word problems that require:
- Reading comprehension of word problems
- Mathematical reasoning and problem-solving
- Step-by-step solution processes
- Final numerical answers

The dataset contains 8,000+ problems, with a test set of problems for evaluation.

## Data Format

### Benchmark data format

Tasks are stored as JSONL in the `data/test.jsonl` file with the following structure:
```json
{
  "question": "Janet's dogs eat 2 cups of dog food each day. Janet has 5 dogs. How many cups of dog food does Janet need to feed her dogs for 3 days?",
  "answer": "Janet has 5 dogs and each dog eats 2 cups of dog food each day. So Janet needs 5 * 2 = 10 cups of dog food each day. For 3 days, Janet needs 10 * 3 = 30 cups of dog food.\n#### 30"
}
```

<br>

### Model output data

The script **run_gpt41_on_gsm8k.py** runs the GPT-4.1 model on the GSM8K test dataset (1319 questions, or a random subset of it), and saves the model responses to an output file named **gsm8k_gpt-4.1_answers.jsonl**, which has a format similar to the **benchmarks/gsm8k/data/test.jsonl** file.

```json
{
  "question_id": "0001",
  "question": "Janet's dogs eat 2 cups of dog food each day. Janet has 5 dogs. How many cups of dog food does Janet need to feed her dogs for 3 days?",
  "answer": "Janet has 5 dogs and each dog eats 2 cups of dog food each day. So Janet needs 5 * 2 = 10 cups of dog food each day. For 3 days, Janet needs 10 * 3 = 30 cups of dog food.\n#### 30"
}
```

This output file is used by the **examples/example_gsm8k.py** script to evaluate the GPT-4.1 model against the GSM8K benchmark.

<br>

## Usage

```python
from benchmarks.gsm8k.gsm8k_benchmark import GSM8KBenchmark

# Initialize the benchmark
benchmark = GSM8KBenchmark()

# Get all task IDs
task_ids = benchmark.get_task_ids()

# Get a specific task
task = benchmark.get_task(task_id)

# Evaluate an answer
result = benchmark.evaluate(task_id, "The answer is 30\n#### 30")
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")
```


<br>

## Evaluation

The GSM8K benchmark uses exact match evaluation for the final numerical answer:

1. **Exact Match (Score: 1.0)**: The final answer matches the expected number
2. **No Match (Score: 0.0)**: The final answer doesn't match

The evaluator extracts the final answer from the output text using the pattern `#### <number>` and checks if it matches the expected answer.

## Answer Format

All GSM8K problems require:
- Step-by-step reasoning process
- Final numerical answer in the format `#### <number>`

The benchmark will:
- Look for the pattern `#### <number>` in the output
- Extract the number after `####`
- Compare it with the expected answer
- If no `####` pattern is found, use the entire output as the answer

## Examples

```python
# Problem: Janet's dogs eat 2 cups of dog food each day. Janet has 5 dogs. How many cups of dog food does Janet need to feed her dogs for 3 days?

result = benchmark.evaluate("0000", "Janet has 5 dogs and each dog eats 2 cups of dog food each day. So Janet needs 5 * 2 = 10 cups of dog food each day. For 3 days, Janet needs 10 * 3 = 30 cups of dog food.\n#### 30")
# Score: 1.0 (Correct!)

result = benchmark.evaluate("0000", "The answer is 30")
# Score: 0.0 (No #### pattern found)

result = benchmark.evaluate("0000", "Janet needs 30 cups of dog food.\n#### 30")
# Score: 1.0 (Correct!)
```

## Task Structure

Each task contains:
- **question**: The word problem text
- **answer**: The expected solution with reasoning and final answer

Task IDs are formatted as `XXXX` where XXXX is a zero-padded index.

## Notes

- Problems cover various mathematical topics including arithmetic, algebra, and word problems
- Solutions should include step-by-step reasoning
- Final answers must be in the format `#### <number>`
- The benchmark evaluates only the final numerical answer, not the reasoning process
- Problems are designed for grade school level mathematical reasoning 