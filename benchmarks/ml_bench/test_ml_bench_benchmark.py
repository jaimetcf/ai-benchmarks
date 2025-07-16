import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from benchmarks.ml_bench.ml_bench_benchmark import MLBenchBenchmark
from core.models.task import Task, EvaluationResult


class TestMLBenchBenchmark(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test data
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_dir = Path(self.temp_dir)
        
        # Create sample test data
        self.sample_data = [
            {
                "instruction": "Train a model with learning rate 0.001",
                "oracle": "python train.py --lr 0.001",
                "output": "python train.py --lr 0.001",
                "type": "Bash Script",
                "arguments": "{'lr': '0.001'}",
                "prefix_code": "",
                "github": "https://github.com/test/repo",
                "path": "./train.py",
                "id": 1
            },
            {
                "instruction": "Install torch package",
                "oracle": "pip install torch",
                "output": "pip install torch",
                "type": "Bash Script",
                "arguments": "{'package': 'torch'}",
                "prefix_code": "",
                "github": "https://github.com/test/repo2",
                "path": "./",
                "id": 2
            }
        ]
        
        # Create test.jsonl file
        self.test_jsonl_path = self.test_data_dir / "test.jsonl"
        with open(self.test_jsonl_path, 'w', encoding='utf-8') as f:
            for data in self.sample_data:
                f.write(json.dumps(data) + '\n')
    
    def tearDown(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_initialization_with_custom_data_dir(self):
        """Test that MLBenchBenchmark initializes with custom data directory."""
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        self.assertEqual(benchmark.name, "ML-Bench")
        self.assertEqual(benchmark.data_dir, self.test_data_dir)
    
    def test_name_property(self):
        """Test that the name property returns the correct benchmark name."""
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        self.assertEqual(benchmark.name, "ML-Bench")
    
    def test_load_tasks(self):
        """Test that tasks are loaded correctly from test.jsonl."""
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        tasks = benchmark._tasks
        
        self.assertEqual(len(tasks), 2)
        
        # Check first task
        task_0000 = tasks["0000"]
        self.assertIsInstance(task_0000, Task)
        self.assertEqual(task_0000.task_id, "0000")
        self.assertEqual(task_0000.benchmark, "ML-Bench")
        self.assertEqual(task_0000.data["instruction"], "Train a model with learning rate 0.001")
        self.assertEqual(task_0000.data["output"], "python train.py --lr 0.001")
        self.assertEqual(task_0000.data["type"], "Bash Script")
        self.assertEqual(task_0000.data["id"], 1)
        
        # Check second task
        task_0001 = tasks["0001"]
        self.assertIsInstance(task_0001, Task)
        self.assertEqual(task_0001.task_id, "0001")
        self.assertEqual(task_0001.data["instruction"], "Install torch package")
        self.assertEqual(task_0001.data["output"], "pip install torch")
    
    def test_get_task_ids(self):
        """Test that get_task_ids returns all task IDs."""
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        task_ids = benchmark.get_task_ids()
        
        self.assertEqual(len(task_ids), 2)
        self.assertIn("0000", task_ids)
        self.assertIn("0001", task_ids)
    
    def test_get_task_valid_id(self):
        """Test that get_task returns the correct task for valid ID."""
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        task = benchmark.get_task("0000")
        
        self.assertIsInstance(task, Task)
        self.assertEqual(task.task_id, "0000")
        self.assertEqual(task.data["instruction"], "Train a model with learning rate 0.001")
    
    def test_get_task_invalid_id(self):
        """Test that get_task raises ValueError for invalid task ID."""
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        
        with self.assertRaises(ValueError) as context:
            benchmark.get_task("9999")
        
        self.assertIn("Task 9999 not found", str(context.exception))
    
    @patch('benchmarks.ml_bench.utils.code_comparer.CodeComparer')
    def test_evaluate_exact_match(self, mock_code_comparer):
        """Test evaluation when generated code matches ground truth exactly."""
        # Mock the code comparer response
        mock_comparer_instance = MagicMock()
        mock_comparer_instance.compare.return_value = {
            "sameResult": True,
            "reason": "Both codes are identical and will produce the same output."
        }
        mock_code_comparer.return_value = mock_comparer_instance
        
        benchmark = MLBenchBenchmark(data_dir=self.test_data_dir)
        result = benchmark.evaluate("0000", "python train.py --lr 0.001")
        
        self.assertIsInstance(result, EvaluationResult)
        self.assertEqual(result.score, 1.0)
        
        # Verify that code comparer was called with correct arguments
        mock_comparer_instance.compare.assert_called_once_with(
            "python train.py --lr 0.001",
            "python train.py --lr 0.001"
        )
    


if __name__ == '__main__':
    unittest.main() 