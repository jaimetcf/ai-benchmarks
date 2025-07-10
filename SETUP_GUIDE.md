# AI Benchmarks - Setup Guide

## Overview

This repository contains a collection of AI agent benchmarks organized as a modular package system. Each benchmark can be installed independently with only its required dependencies.

## Structure

```
ai-benchmarks/
├── pyproject.toml          # Main package with optional dependencies
├── core/                   # Core interfaces and models (minimal dependencies)
├── benchmarks/
│   ├── aime2025/          # AIME 2025 benchmark (no external deps)
│   ├── gaia/              # GAIA benchmark (no external deps)
│   └── swebench/          # SWE-bench (requires docker, datasets, etc.)
└── examples/              # Usage examples
```

## Installation Options

### 1. Install Core Only (for developing new benchmarks)
```bash
uv pip install -e .
```

### 2. Install Specific Benchmarks
```bash
# Install core + AIME benchmark only
uv pip install -e ".[aime]"

# Install core + GAIA benchmark only
uv pip install -e ".[gaia]"

# Install core + SWE-bench only (includes heavy dependencies)
uv pip install -e ".[swebench]"
```

### 3. Install Multiple Benchmarks
```bash
# Install AIME and GAIA (lightweight benchmarks)
uv pip install -e ".[aime,gaia]"
```

### 4. Install Everything
```bash
uv pip install -e ".[all]"
```

## Usage in Other Projects

### Option 1: Install from Local Path
```bash
# In your project
uv pip install -e "/path/to/ai-benchmarks[aime]"
```

### Option 2: Install from Git (once published)
```bash
uv pip install "git+https://github.com/yourusername/ai-benchmarks.git#egg=ai-benchmarks[aime]"
```

### Option 3: Dependencies Only
If you just want to install dependencies for a benchmark without the package:
```bash
# Install only SWE-bench dependencies
uv pip install datasets docker modal huggingface-hub
```

## Using in Your Code

```python
# Core components are always available
from core import BaseBenchmark, Task, EvaluationResult

# Specific benchmarks (only if installed)
try:
    from benchmarks.aime2025 import AIMEBenchmark
    aime = AIMEBenchmark()
except ImportError:
    print("AIME benchmark not installed. Install with: uv pip install -e '.[aime]'")

# Get tasks
task_ids = aime.get_task_ids()
task = aime.get_task(task_ids[0])

# Evaluate
result = aime.evaluate(task_ids[0], "42")
print(f"Score: {result.score}")
print(f"Explanation: {result.score_explanation}")
```

## Benefits of This Structure

1. **Minimal Dependencies**: Installing AIME doesn't require Docker or other heavy dependencies from SWE-bench
2. **Modular**: Each benchmark is self-contained with its own dependencies
3. **Flexible**: Can install only what you need
4. **Easy to Extend**: Adding new benchmarks follows the same pattern

## Adding a New Benchmark

1. Create a new directory under `benchmarks/`
2. Implement the benchmark extending `BaseBenchmark` or `CodeExecutionBenchmark`
3. Update the root `pyproject.toml` to add any benchmark-specific dependencies:
   ```toml
   [project.optional-dependencies]
   your_benchmark = ["dependency1", "dependency2"]
   all = [...existing..., "dependency1", "dependency2"]
   ```

## Development Setup

For development, install in editable mode with all benchmarks:
```bash
uv pip install -e ".[all]"
```

## Troubleshooting

### Import Errors
If you get import errors for specific benchmarks, ensure you've installed them:
```bash
# Check installed packages
uv pip list | grep ai-benchmarks

# Install missing benchmark
uv pip install -e ".[benchmark_name]"
```

### Path Issues
The benchmarks now use relative paths for their data files. If you need to specify custom data directories:

```python
# Use default data directory (relative to benchmark module)
aime = AIMEBenchmark()

# Or specify custom path
aime = AIMEBenchmark(data_dir="/custom/path/to/aime/tasks")
``` 