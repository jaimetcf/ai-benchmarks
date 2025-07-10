# Guide: Adding a New Benchmark

This guide explains how to add a new benchmark to the AI Benchmarks repository. Follow these steps to maintain consistency with existing benchmarks.

## Overview

Each benchmark should:
1. Live in its own directory under `benchmarks/`
2. Inherit from either `BaseBenchmark` (for simple evaluation) or `CodeExecutionBenchmark` (for execution-based evaluation)
3. Implement the required interface methods
4. Follow the existing naming and structure patterns

## Step-by-Step Instructions

### 1. Create the Benchmark Directory

```bash
mkdir benchmarks/your_benchmark_name
```

Use lowercase with underscores for the directory name (e.g., `agent_company`, `browser_comp`).

### 2. Create the Benchmark Implementation

Create `benchmarks/your_benchmark_name/your_benchmark.py`:

```python
from pathlib import Path
from typing import Any

from benchmarks.core.base_benchmark import BaseBenchmark  # or CodeExecutionBenchmark
from benchmarks.core.models.task import EvaluationResult, Task


class YourBenchmarkName(BaseBenchmark):
    """Description of what your benchmark evaluates."""
    
    def __init__(self, data_dir: str | None = None):
        """Initialize the benchmark.
        
        Args:
            data_dir: Optional path to data directory. If None, uses default.
        """
        if data_dir is None:
            # Use path relative to this file
            data_dir = Path(__file__).parent / "data"  # or "tasks", "files", etc.
        self.data_dir = Path(data_dir)
        self._tasks = self._load_tasks()
    
    @property
    def name(self) -> str:
        """Return the benchmark name."""
        return "YourBenchmarkName"
    
    def get_task_ids(self) -> list[str]:
        """Return all task IDs."""
        return list(self._tasks.keys())
    
    def get_task(self, task_id: str) -> Task:
        """Get a specific task by ID."""
        if task_id not in self._tasks:
            raise ValueError(f"Task {task_id} not found")
        return self._tasks[task_id]
    
    def evaluate(self, task_id: str, output: Any) -> EvaluationResult:
        """Evaluate the model output for a task.
        
        Args:
            task_id: The task ID to evaluate
            output: The model's output
            
        Returns:
            EvaluationResult with score and explanation
        """
        task = self.get_task(task_id)
        expected = task.data.get("expected_answer", "")  # Adjust based on your data
        
        # Implement your evaluation logic here
        if str(output).strip() == str(expected).strip():
            return EvaluationResult(
                score=1.0,
                score_explanation="Correct answer"
            )
        else:
            return EvaluationResult(
                score=0.0,
                score_explanation=f"Expected: {expected}, Got: {output}"
            )
    
    def _load_tasks(self) -> dict[str, Task]:
        """Load tasks from data files."""
        tasks = {}
        
        # Example: Load from JSON files
        # for json_file in self.data_dir.glob("*.json"):
        #     with open(json_file) as f:
        #         data = json.load(f)
        #         task = Task(
        #             task_id=data["id"],
        #             benchmark=self.name,
        #             data=data
        #         )
        #         tasks[task.task_id] = task
        
        return tasks
```

### 3. Create the `__init__.py` File

Create `benchmarks/your_benchmark_name/__init__.py`:

```python
from .your_benchmark import YourBenchmarkName

__all__ = ["YourBenchmarkName"]
```

### 4. Update Root `pyproject.toml`

Add your benchmark's dependencies (if any) to the root `pyproject.toml`:

```toml
[project.optional-dependencies]
# ... existing entries ...
your_benchmark = ["dependency1>=version", "dependency2>=version"]  # Add if needed
all = [
    # ... existing dependencies ...
    "dependency1>=version",  # Add your dependencies here too
    "dependency2>=version",
]
```

If your benchmark has no external dependencies, just add an empty list:
```toml
your_benchmark = []  # No external dependencies
```

### 5. Update Root `__init__.py`

Add your benchmark to the root `__init__.py` so it's imported when available:

```python
# Add this try-except block after the existing ones
try:
    from benchmarks.your_benchmark_name import YourBenchmarkName
    __all__.append("YourBenchmarkName")
except ImportError:
    pass
```

### 6. Add Data Files

Create a data directory in your benchmark folder and add your task data:

```
benchmarks/your_benchmark_name/
├── __init__.py
├── your_benchmark.py
└── data/           # or tasks/, files/, etc. - whatever makes sense
    ├── task1.json
    ├── task2.json
    └── ...
```

### 7. Create Tests (Recommended)

Create `benchmarks/your_benchmark_name/test_your_benchmark.py`:

```python
import unittest
from benchmarks.your_benchmark_name import YourBenchmarkName


class TestYourBenchmark(unittest.TestCase):
    def setUp(self):
        self.benchmark = YourBenchmarkName()
    
    def test_get_task_ids(self):
        task_ids = self.benchmark.get_task_ids()
        self.assertIsInstance(task_ids, list)
        self.assertGreater(len(task_ids), 0)
    
    def test_get_task(self):
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task = self.benchmark.get_task(task_ids[0])
            self.assertEqual(task.benchmark, "YourBenchmarkName")
    
    def test_evaluate(self):
        # Add specific evaluation tests
        pass


if __name__ == "__main__":
    unittest.main()
```

### 8. Create Documentation

Create `benchmarks/your_benchmark_name/README.md`:

```markdown
# Your Benchmark Name

## Overview
Brief description of what this benchmark evaluates and why it's important.

## Task Structure
Explain the structure of tasks in this benchmark.

## Evaluation Metrics
Describe how tasks are evaluated and scored.

## Usage Example
```python
from benchmarks.your_benchmark_name import YourBenchmarkName

benchmark = YourBenchmarkName()
task_ids = benchmark.get_task_ids()
task = benchmark.get_task(task_ids[0])

# Evaluate
result = benchmark.evaluate(task_ids[0], "model output")
print(f"Score: {result.score}")
```

## Dataset Information
- Number of tasks: X
- Task types: ...
- Sources: ...
```

### 9. Add an Example

Create `examples/example_your_benchmark.py`:

```python
"""Example usage of YourBenchmarkName."""

from benchmarks.your_benchmark_name import YourBenchmarkName


def main():
    # Initialize benchmark
    benchmark = YourBenchmarkName()
    
    # Get task information
    task_ids = benchmark.get_task_ids()
    print(f"Total tasks: {len(task_ids)}")
    
    # Example with first task
    if task_ids:
        task_id = task_ids[0]
        task = benchmark.get_task(task_id)
        
        print(f"\nTask ID: {task_id}")
        print(f"Task data keys: {list(task.data.keys())}")
        
        # Example evaluation
        example_output = "example answer"
        result = benchmark.evaluate(task_id, example_output)
        
        print(f"\nEvaluation result:")
        print(f"Score: {result.score}")
        print(f"Explanation: {result.score_explanation}")


if __name__ == "__main__":
    main()
```

## Special Cases

### For Execution-Based Benchmarks

If your benchmark requires code execution (like SWE-bench), inherit from `CodeExecutionBenchmark` instead:

```python
from benchmarks.core.base_benchmark import CodeExecutionBenchmark
from benchmarks.core.models.task import TaskResult, ExecutionResult, EvaluationResult


class YourExecutionBenchmark(CodeExecutionBenchmark):
    def evaluate_with_execution(self, task_id: str, output: Any, **kwargs) -> TaskResult:
        """Evaluate with code execution.
        
        Args:
            task_id: Task to evaluate
            output: Model output (e.g., code)
            **kwargs: Additional parameters (timeout, etc.)
            
        Returns:
            TaskResult with execution details
        """
        # Implement execution logic
        # Return TaskResult with ExecutionResult and EvaluationResult
        pass
```

### Task Data Structure

The `Task` object uses a flexible `data` dictionary. Common patterns:

```python
# AIME style - mathematical problems
task.data = {
    "task_id": "problem_001",
    "question": "Solve for x...",
    "ground_truth": "42",
    "domain": "algebra",
}

# GAIA style - general tasks
task.data = {
    "task_id": "task_001", 
    "Question": "What is...",
    "Final answer": "expected answer",
    "Level": 1,  # difficulty
    "file_name": "data.csv",  # if task has files
}

# SWE-bench style - code tasks
task.data = {
    "instance_id": "repo__issue-123",
    "problem_statement": "Bug description...",
    "patch": "Expected fix...",
    "repo": "owner/repo",
}
```

## Naming Conventions

- **Directory**: lowercase with underscores (e.g., `agent_company`)
- **Class name**: PascalCase ending with "Benchmark" (e.g., `AgentCompanyBenchmark`)
- **Module name**: lowercase with underscores (e.g., `agent_company_benchmark.py`)
- **Benchmark name property**: Human-readable (e.g., `"AgentCompany"`)

## Common Patterns to Follow

1. **Data Loading**: Load all tasks in `__init__` and cache them
2. **Error Handling**: Raise `ValueError` for invalid task IDs
3. **Path Handling**: Use `Path` objects and relative paths
4. **Type Hints**: Use proper type annotations throughout
5. **Docstrings**: Document all public methods

## Testing Your Benchmark

After implementation:

```bash
# Install with your benchmark
uv pip install -e ".[your_benchmark]"

# Test imports
python -c "from benchmarks.your_benchmark_name import YourBenchmarkName"

# Run tests
python benchmarks/your_benchmark_name/test_your_benchmark.py

# Run example
python examples/example_your_benchmark.py
```

## Final Checklist

- [ ] Created benchmark directory under `benchmarks/`
- [ ] Implemented benchmark class inheriting from appropriate base class
- [ ] Created `__init__.py` with proper exports
- [ ] Added dependencies to root `pyproject.toml` (if any)
- [ ] Updated root `__init__.py` with try-except import
- [ ] Added task data files
- [ ] Created tests
- [ ] Created README documentation
- [ ] Added usage example
- [ ] Tested installation and imports

## See Also

- [BENCHMARK_EXAMPLES.md](BENCHMARK_EXAMPLES.md) - Concrete examples for AgentCompany and BrowserComp benchmarks
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation and usage guide
- [README.md](README.md) - Main repository documentation 