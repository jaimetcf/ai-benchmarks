import unittest
from benchmarks.gsm8k import GSM8KBenchmark


class TestGSM8KBenchmark(unittest.TestCase):
    """Test cases for BrowseComp benchmark."""

    def setUp(self):
        self.benchmark = GSM8KBenchmark()

    def test_benchmark_name(self):
        """Test that benchmark name is correct."""
        self.assertEqual(self.benchmark.name, "GSM8K")

    def test_get_task_ids(self):
        """Test getting task IDs."""
        task_ids = self.benchmark.get_task_ids()
        self.assertIsInstance(task_ids, list)
        self.assertGreater(len(task_ids), 0, "Should have at least one task")
        # Check task ID format
        for task_id in task_ids[:5]:  # Check first 5
            self.assertTrue(convert_string_to_integer(task_id) is not None)

    def test_get_task(self):
        """Test getting individual tasks."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            task = self.benchmark.get_task(task_id)

            # Check task structure
            self.assertEqual(task.task_id, task_id)
            self.assertEqual(task.benchmark, "GSM8K")
            self.assertIsInstance(task.data, dict)

            # Check required fields
            self.assertIn("question", task.data)
            self.assertIn("answer", task.data)

    def test_get_invalid_task(self):
        """Test getting invalid task raises error."""
        with self.assertRaises(ValueError):
            self.benchmark.get_task("invalid_task_id")

    def test_evaluate_correct_answers(self):
        """Test evaluation with correct answers."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            result = self.benchmark.evaluate(task_id, "#### 18")
            self.assertEqual(result.score, 1.0)
            self.assertEqual("Correct answer", result.score_explanation)

            task_id = task_ids[11]
            result = self.benchmark.evaluate(task_id, "#### 694")
            self.assertEqual(result.score, 1.0)
            self.assertEqual("Correct answer", result.score_explanation)

            task_id = task_ids[99]
            result = self.benchmark.evaluate(task_id, "#### 58")
            self.assertEqual(result.score, 1.0)
            self.assertEqual("Correct answer", result.score_explanation)

    def test_evaluate_wrong_answers(self):
        """Test evaluation with correct answers."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            result = self.benchmark.evaluate(task_id, "#### 25")
            self.assertEqual(result.score, 0.0)
            self.assertEqual("Expected: 18, Got: 25", result.score_explanation)

            task_id = task_ids[11]
            result = self.benchmark.evaluate(task_id, "#### 102")
            self.assertEqual(result.score, 0.0)
            self.assertEqual("Expected: 694, Got: 102", result.score_explanation)

            task_id = task_ids[99]
            result = self.benchmark.evaluate(task_id, "#### -2")
            self.assertEqual(result.score, 0.0)
            self.assertEqual("Expected: 58, Got: -2", result.score_explanation)



def convert_string_to_integer(string_value, default=None):
    try:
        # Remove whitespace
        cleaned = string_value.strip()
        
        # Handle empty strings
        if not cleaned:
            return default
            
        # Try conversion
        return int(cleaned)
            
    except (ValueError, TypeError):
        return default

if __name__ == "__main__":
    unittest.main()
