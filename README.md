# AI Benchmarks

A modular collection of standardized benchmarks for evaluating AI models. Each benchmark can be installed independently with only its required dependencies.

## Quick Start

```bash
# Install only the benchmarks you need
uv pip install -e ".[aime]"        # Just AIME (no external deps)
uv pip install -e ".[gaia]"        # Just GAIA (no external deps)
uv pip install -e ".[swebench]"    # Just SWE-bench (Docker, datasets, etc.)
uv pip install -e ".[all]"         # Everything

# Check what's installed
python examples/modular_usage_example.py
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation and usage instructions.

## Available Benchmarks

### AIME (American Invitational Mathematics Examination)
- Mathematical problem-solving benchmark
- 30 problems from AIME 2025 (15 from each exam)
- Integer answers between 0-999
- See `AIME2025/README.md` for details

### GAIA (General AI Assistants)
- Real-world task benchmark requiring various capabilities
- 466 tasks across 3 difficulty levels
- Tasks may include file analysis, web search, multi-step reasoning
- See `GAIA/README.md` for details

### SWE-bench (Software Engineering Benchmark)
- Code generation benchmark for real-world software issues
- Requires generating patches to fix bugs in open-source repositories
- Includes test execution to verify correctness
- See `swebench/README.md` for details

### GSM8K (Grade School Math 8K)
- Math word problem benchmark for grade school students
- 8,000 word problems from the 2019 Grade School Math Competition
- See `gsm8k/README.md` for detailsThe GSM8K (Grade School Math 8K) benchmark tests mathematical reasoning abilities on grade school word problems.

### ML-Bench (Machine Learning Benchmark)
- The ML-Bench benchmark tests machine learning code generation abilities by evaluating how well models can generate executable code for various machine learning tasks based on natural language instructions.
- See `ml_bench/README.md` for details

<br>

## Unified Interface

All benchmarks implement a common interface defined in `base_benchmark.py`:

### Base Interface (All Benchmarks)

```python
# Core components (always available)
from core import BaseBenchmark, Task, EvaluationResult

# Specific benchmark (if installed)
from benchmarks.aime2025 import AIMEBenchmark
from benchmarks.gaia import GAIABenchmark
from benchmarks.swebench import SWEBenchVerified

# Initialize
benchmark = AIMEBenchmark()  # or GAIABenchmark(), SWEBenchVerified()

# Get tasks
task_ids = benchmark.get_task_ids()
task = benchmark.get_task(task_id)

# Evaluate - common interface for all benchmarks
result = benchmark.evaluate(task_id, model_output)
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")
```

### Extended Interface (Execution-Based Benchmarks)

Benchmarks like SWE-bench that require code execution extend the base interface:

```python
# For detailed execution results
if hasattr(benchmark, 'evaluate_with_execution'):
    task_result = benchmark.evaluate_with_execution(
        task_id=task_id,
        output=model_output,
        use_modal=True  # or other execution parameters
    )
    print(f"Execution time: {task_result.execution.execution_time}")
    print(f"Execution trace: {task_result.execution.execution_trace}")
```

## Benchmark Types

### Simple Evaluation Benchmarks
- **AIME**: Compare numeric answers
- **GAIA**: Compare text answers with normalization

These benchmarks inherit from `BaseBenchmark` and implement simple answer comparison.

### Execution-Based Benchmarks
- **SWE-bench**: Execute code patches and run tests

These benchmarks inherit from `ExecutionBasedBenchmark` and provide both:
- Simple `evaluate()` interface for compatibility
- Extended `evaluate_with_execution()` for detailed results

## Usage Examples

See the `examples/` directory for complete examples:

- `example_aime.py` - AIME usage example
- `example_gaia.py` - GAIA usage example  
- `unified_example.py` - Shows unified interface across all benchmarks

Run examples from the project root:
```bash
python -m benchmarks.examples.example_aime
python -m benchmarks.examples.example_gaia
python -m benchmarks.examples.unified_example
python -m benchmarks.examples.example_evaluate_gpt41_on_gsm8k
python -m benchmarks.examples.example_evaluate_gpt41_on_ml_bench
```

## Directory Structure

```
ai-benchmarks/
├── pyproject.toml      # Root package with optional extras
├── core/               # Core interfaces and models (minimal deps)
│   ├── __init__.py
│   ├── base_benchmark.py
│   └── models/
│       └── task.py
├── benchmarks/
│   ├── aime2025/       # AIME benchmark (no external deps)
│   │   ├── aime_benchmark.py
│   │   └── tasks/
│   ├── gaia/           # GAIA benchmark (no external deps)
│   │   ├── gaia_benchmark.py
│   │   └── files/
│   ├── gsm8k/          # GSM8K benchmark (no external deps)
│   │   ├── gsm8k_benchmark.py
│   │   └── data/
│   ├── ml_bench/       # ML-Bench benchmark (no external deps)
│   │   ├── ml_bench_benchmark.py
│   │   ├── data/
│   │   └── utils/
│   └── swebench/       # SWE-bench (Docker, datasets, etc.)
│       ├── swebench.py
│       └── harness/
|    
└── examples/           # Usage examples
    ├── example_aime.py
    ├── example_gaia.py
    ├── example_evaluate_gpt41_on_gsm8k.py
    ├── example_evaluate_gpt41_on_ml_bench.py
    ├── unified_example.py
    └── modular_usage_example.py
```

## Adding New Benchmarks

To add a new benchmark, see the comprehensive guide: [ADD_NEW_BENCHMARK_GUIDE.md](ADD_NEW_BENCHMARK_GUIDE.md)

Quick overview:
1. Create directory under `benchmarks/your_benchmark_name`
2. Implement class inheriting from `BaseBenchmark` or `CodeExecutionBenchmark`
3. Add dependencies to root `pyproject.toml` (if any)
4. Update root `__init__.py` with try-except import
5. Add tests, documentation, and examples 