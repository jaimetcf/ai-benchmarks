# ML-Bench Benchmark

The ML-Bench benchmark tests machine learning code generation abilities by evaluating how well models can generate executable code for various machine learning tasks based on natural language instructions.

## Structure

The ML-Bench benchmark consists of machine learning code generation tasks that require:
- Understanding natural language instructions for ML tasks
- Generating executable Python code or bash commands
- Working with various ML frameworks and libraries
- Handling different types of ML tasks (training, inference, data processing, etc.)

The dataset contains 260 tasks covering various machine learning domains including:
- Graph Neural Networks (DGL, PyTorch Geometric)
- Natural Language Processing (BERT, Transformers)
- Computer Vision (OpenCLIP, LAVIS)
- Protein Structure Prediction (ESM)
- Time Series Analysis
- And many more

## Data Format

### Benchmark data format

Tasks are stored as JSONL in the `data/test.jsonl` file with the following structure:
```json
{
  "github": "https://github.com/dmlc/dgl",
  "path": "./examples/pytorch/arma",
  "arguments": "{'dataset': 'Citeseer', 'lr': '0', 'num-stacks': '5'}",
  "instruction": "Can you help me by formulating the necessary code to utilize the Citeseer dataset as the training data to empower the ARMA model with a learning rate set to 0 and incorporate 5 stacks into the model? Your assistance would be greatly appreciated.",
  "oracle": "The following commands learn a neural network and predict on the test set. Train an ARMA model which follows the original hyperparameters on different datasets.\n\n# Cora:\npython citation.py --gpu 0\n\n# Citeseer:\npython citation.py --gpu 0 --dataset Citeseer --num-stacks 3\n\n# Pubmed:\npython citation.py --gpu 0 --dataset Pubmed --dropout 0.25 --num-stacks 1",
  "type": "Bash Script",
  "output": "python citation.py --dataset Citeseer --lr 0 --num-stacks 5"
}
```

### Model output data

The script **run_gpt41_on_ml_bench.py** runs the GPT-4.1 model on the ML-Bench test dataset (260 questions, or a random subset of it), and saves the model responses to an output file named **ml_bench_gpt-4.1_answers.jsonl**, which has a format similar to the **benchmarks/ml_bench/data/test.jsonl** file.

```json
{
  "question_id": "0001",
  "question": "For executing the instruction below in this prompt, you will consult the code in the following github file https://github.com/dmlc/dgl/./examples/pytorch/arma\nThe arguments for the script are: {'dataset': 'Citeseer', 'lr': '0', 'num-stacks': '5'}\nThe instruction is: Can you help me by formulating the necessary code to utilize the Citeseer dataset as the training data to empower the ARMA model with a learning rate set to 0 and incorporate 5 stacks into the model? Your assistance would be greatly appreciated.",
  "answer": "python citation.py --dataset Citeseer --lr 0 --num-stacks 5"
}
```

This output file is used by the **examples/example_evaluate_gpt41_on_ml_bench.py** script to evaluate the GPT-4.1 model against the ML-Bench benchmark.

## Usage

```python
from benchmarks.ml_bench.ml_bench_benchmark import MLBenchBenchmark

# Initialize the benchmark
benchmark = MLBenchBenchmark()

# Get all task IDs
task_ids = benchmark.get_task_ids()

# Get a specific task
task = benchmark.get_task(task_id)

# Evaluate an answer
result = benchmark.evaluate(task_id, "python citation.py --dataset Citeseer --lr 0 --num-stacks 5")
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")
```

## Evaluation

The ML-Bench benchmark uses semantic code comparison evaluation:

1. **Exact Match (Score: 1.0)**: The generated code produces the same output as the expected code
2. **Semantic Match (Score: 1.0)**: The generated code is functionally equivalent to the expected code
3. **No Match (Score: 0.0)**: The generated code is not functionally equivalent

The evaluator uses GPT-4.1 to compare the generated code with the expected code and determine if they produce the same output or are functionally equivalent.

## Code Generation Requirements

All ML-Bench tasks require:
- Executable Python code or bash commands
- Correct handling of specified parameters and arguments
- Proper use of the target ML framework/library
- Functional equivalence to the expected output

The benchmark evaluates:
- Code correctness and functionality
- Parameter handling
- Framework/library usage
- Output equivalence

## Examples

```python
# Task: Generate code to train an ARMA model on Citeseer dataset
# Expected: python citation.py --dataset Citeseer --lr 0 --num-stacks 5

result = benchmark.evaluate("0001", "python citation.py --dataset Citeseer --lr 0 --num-stacks 5")
# Score: 1.0 (Correct!)

result = benchmark.evaluate("0001", "python citation.py --dataset Citeseer")
# Score: 0.0 (Missing required parameters)

result = benchmark.evaluate("0001", "python train.py --dataset Citeseer --lr 0 --num-stacks 5")
# Score: 0.0 (Wrong script name)
```

## Task Structure

Each task contains:
- **github**: The GitHub repository URL
- **path**: The specific path within the repository
- **arguments**: Required arguments for the task
- **instruction**: Natural language description of the task
- **oracle**: Documentation or examples for the task
- **type**: Type of code expected (Python code, Bash script, etc.)
- **output**: The expected correct output

Task IDs are formatted as `XXXX` where XXXX is a zero-padded index.

## Supported Frameworks and Libraries

The benchmark covers a wide range of ML frameworks and libraries:
- **Graph Neural Networks**: DGL, PyTorch Geometric
- **NLP**: BERT, Transformers, ESM
- **Computer Vision**: OpenCLIP, LAVIS, DeepFloyd IF
- **Time Series**: Time-Series-Library
- **GANs**: PyTorch-GAN implementations
- **And many more**

## Notes

- Tasks require understanding of specific ML frameworks and their APIs
- Generated code must be executable and produce the expected output
- The benchmark evaluates both code correctness and functional equivalence
- Tasks cover various difficulty levels from simple parameter setting to complex model training
- The evaluation uses semantic comparison rather than exact string matching
- All tasks are derived from real-world machine learning repositories and use cases 