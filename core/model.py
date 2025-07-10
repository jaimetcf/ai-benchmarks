import os
import json
from core.base_benchmark import BaseBenchmark


class Model():
    """
    A model is a class that represents a generative AI model that can be evaluated on a benchmark.
    It is initialized with a name and a benchmark.
    It has a method to load the answers from a file, and a method to evaluate the model on the benchmark.
    """
    def __init__(self, name: str, benchmark: BaseBenchmark, logfile_folder: str = "."):
        self.name = name.lower()
        self.benchmark = benchmark
        self.logfile_folder = logfile_folder
        self._answers = []
        self.load_answers()

    def load_answers(self):
        # Get the absolute path to the answers file
        answers_path = os.path.join(os.path.dirname(__file__), 
            '..', 'benchmarks', 
            f'{self.benchmark.name.lower()}', 
            'data', 
            f'{self.benchmark.name.lower()}_{self.name}_answers.jsonl'
        )
        answers_path = os.path.abspath(answers_path)
        answers = []
        with open(answers_path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = json.loads(line)
                answers.append(obj)
        self._answers = answers

    def getQuestionIds(self):
        return [obj["question_id"] for obj in self._answers if "question_id" in obj]

    def solve(self, question_id):
        for obj in self._answers:
            if obj.get("question_id") == question_id:
                return obj.get("answer", "")
        return ""

    def evaluate_on_benchmark(self):
        task_ids = self.getQuestionIds()
        print(f'Evaluating {self.name} on {self.benchmark.name.lower()}...')

        # Create log file name based on model name and logfile_folder
        log_filename = os.path.join(
            self.logfile_folder, f'evaluate_{self.name}_on_{self.benchmark.name.lower()}_log.txt')
        
        total_score = 0
        results = []

        for task_id in task_ids:
            # Get the task
            task = self.benchmark.get_task(task_id)
            # Get the problem text
            problem = task.data["question"]
            # Get the model output
            model_output = self.solve(task_id)
            # Evaluate the output
            result = self.benchmark.evaluate(task_id, model_output)
            # Store results
            total_score += result.score
            results.append({
                "task_id": task_id, 
                "score": result.score, 
                "explanation": result.score_explanation, 
                "model_output": model_output})
            
            # Write individual result to log file
            with open(log_filename, 'a', encoding='utf-8') as f:
                f.write(f"\nTask: {task_id}\n")
                f.write(f"Problem: {problem}...\n")
                f.write(f"Model output: {model_output}\n")
                f.write(f"Score: {result.score}\n")
                f.write(f"Explanation: {result.score_explanation}\n")

        # Calculate and print summary statistics
        accuracy = total_score / len(task_ids) if task_ids else 0
        print("\n" + "=" * 60)
        print(f'Summary: {total_score}/{len(task_ids)} correct ({accuracy:.1%} accuracy)')
        
        # Write summary to log file
        with open(log_filename, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f'Summary: {total_score}/{len(task_ids)} correct ({accuracy:.1%} accuracy)\n')
        
        return results
