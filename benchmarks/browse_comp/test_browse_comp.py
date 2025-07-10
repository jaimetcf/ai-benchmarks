"""Tests for BrowseComp benchmark."""

import unittest
from benchmarks.browse_comp import BrowseCompBenchmark


class TestBrowseCompBenchmark(unittest.TestCase):
    """Test cases for BrowseComp benchmark."""

    def setUp(self):
        """Set up test fixtures."""
        self.benchmark = BrowseCompBenchmark()

    def test_benchmark_name(self):
        """Test that benchmark name is correct."""
        self.assertEqual(self.benchmark.name, "BrowseComp")

    def test_get_task_ids(self):
        """Test getting task IDs."""
        task_ids = self.benchmark.get_task_ids()
        self.assertIsInstance(task_ids, list)
        self.assertGreater(len(task_ids), 0, "Should have at least one task")
        # Check task ID format
        for task_id in task_ids[:5]:  # Check first 5
            self.assertTrue(task_id.startswith("browsecomp_"))

    def test_get_task(self):
        """Test getting individual tasks."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            task = self.benchmark.get_task(task_id)

            # Check task structure
            self.assertEqual(task.task_id, task_id)
            self.assertEqual(task.benchmark, "BrowseComp")
            self.assertIsInstance(task.data, dict)

            # Check required fields
            self.assertIn("question", task.data)
            self.assertIn("answer", task.data)
            self.assertIn("canary", task.data)
            self.assertIn("index", task.data)

    def test_get_invalid_task(self):
        """Test getting invalid task raises error."""
        with self.assertRaises(ValueError):
            self.benchmark.get_task("invalid_task_id")

    def test_evaluate_correct_answer(self):
        """Test evaluation with correct answer."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            task_info = self.benchmark.get_task_info(task_id)
            correct_answer = task_info["answer"]

            # Test exact match in proper format
            output = f"Exact Answer: {correct_answer}"
            result = self.benchmark.evaluate(task_id, output)
            self.assertEqual(result.score, 1.0)
            self.assertIn("Correct", result.score_explanation)

    def test_evaluate_wrong_answer(self):
        """Test evaluation with wrong answer."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]

            # Test clearly wrong answer
            output = "Exact Answer: This is definitely not the right answer"
            result = self.benchmark.evaluate(task_id, output)
            self.assertEqual(result.score, 0.0)
            self.assertIn("Incorrect", result.score_explanation)

    def test_evaluate_none_output(self):
        """Test evaluation with None output."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            result = self.benchmark.evaluate(task_id, None)
            self.assertEqual(result.score, 0.0)

    def test_format_question(self):
        """Test question formatting."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            formatted = self.benchmark.format_question(task_id)

            # Check that formatting template is applied
            self.assertIn("Your response should be in the following format:", formatted)
            self.assertIn("Explanation:", formatted)
            self.assertIn("Exact Answer:", formatted)
            self.assertIn("Confidence:", formatted)

    def test_get_task_info(self):
        """Test getting task info."""
        task_ids = self.benchmark.get_task_ids()
        if task_ids:
            task_id = task_ids[0]
            info = self.benchmark.get_task_info(task_id)

            # Check info structure
            self.assertIsInstance(info, dict)
            self.assertIn("question", info)
            self.assertIn("answer", info)
            self.assertIn("index", info)

    def test_decryption(self):
        """Test the decryption functionality."""
        # Test empty inputs
        self.assertEqual(self.benchmark._decrypt("", ""), "")
        self.assertEqual(self.benchmark._decrypt("test", ""), "")
        self.assertEqual(self.benchmark._decrypt("", "test"), "")

        # Test invalid base64
        self.assertEqual(self.benchmark._decrypt("not-base64!", "password"), "")

    def test_simple_grade(self):
        """Test the simple grading function."""
        # Test exact match
        score = self.benchmark._simple_grade("Exact Answer: test answer", "test answer")
        self.assertGreater(score, 0.5)

        # Test case insensitive
        score = self.benchmark._simple_grade("Exact Answer: TEST ANSWER", "test answer")
        self.assertGreater(score, 0.5)

        # Test partial match
        score = self.benchmark._simple_grade("The answer is test answer somewhere", "test answer")
        self.assertGreater(score, 0)

        # Test no match
        score = self.benchmark._simple_grade("completely different", "test answer")
        self.assertEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
