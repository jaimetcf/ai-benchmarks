# BrowseComp Benchmark

## Overview

BrowseComp is a simple yet challenging benchmark for evaluating browsing agents. It tests an agent's ability to find information on the web and provide accurate answers to questions that require web browsing capabilities.

The benchmark was created by OpenAI and consists of questions that require browsing the web to find answers. Questions and answers are encrypted in the dataset for security purposes.

**Paper/Blog**: [BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents](https://openai.com/index/browsecomp/)

**Authors**: Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jeffrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, Mia Glaese

## Task Structure

Each task in BrowseComp consists of:
- **Question**: An encrypted question that requires web browsing to answer
- **Answer**: The encrypted correct answer
- **Canary**: A password used for decryption

The questions are designed to test various browsing capabilities including:
- Finding specific information on websites
- Navigating through multiple pages
- Understanding and extracting relevant data
- Handling dynamic web content

## Evaluation Metrics

The benchmark uses a binary scoring system:
- **Score 1.0**: Correct answer provided
- **Score 0.0**: Incorrect or incomplete answer

The evaluation checks if the model's output contains the correct answer, with some tolerance for formatting differences.

## Usage Example

```python
from benchmarks.browse_comp import BrowseCompBenchmark

# Initialize the benchmark
benchmark = BrowseCompBenchmark()

# Get all task IDs
task_ids = benchmark.get_task_ids()
print(f"Total tasks: {len(task_ids)}")

# Get a specific task
task_id = task_ids[0]
task = benchmark.get_task(task_id)

# Format the question with the standard template
formatted_question = benchmark.format_question(task_id)
print(f"Question: {formatted_question}")

# Evaluate a response
model_output = """
Explanation: Based on my web search, I found that...
Exact Answer: The answer is 42
Confidence: 85%
"""

result = benchmark.evaluate(task_id, model_output)
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")
```

## Dataset Information

- **Source**: OpenAI's public dataset
- **URL**: https://openaipublic.blob.core.windows.net/simple-evals/browse_comp_test_set.csv
- **Format**: CSV with encrypted questions and answers
- **Security**: Questions and answers are XOR-encrypted with task-specific keys

## Response Format

Models should format their responses using the following template:

```
Explanation: {your explanation for your final answer}
Exact Answer: {your succinct, final answer}
Confidence: {your confidence score between 0% and 100% for your answer}
```

## Notes

- The benchmark automatically downloads the dataset from OpenAI's public URL on first use
- Questions and answers are decrypted on-the-fly during task loading
- The evaluation focuses on the "Exact Answer" field but falls back to checking the entire response
- This implementation provides a simple grading function, but you can extend it to use a more sophisticated grader model if needed 