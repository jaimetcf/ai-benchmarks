"""
This script evaluates the GPT-4.1 model against the GSM8K benchmark.
It produces a final accuracy score and a log file named evaluate_gpt-4.1_on_gsm8k_log.txt, 
which saves the results of the evaluation.
It uses the Model class from the core.models.model module, 
and the GSM8KBenchmark class from the benchmarks.gsm8k.gsm8k_benchmark module.
"""
from benchmarks.gsm8k.gsm8k_benchmark import GSM8KBenchmark
from core.model import Model


def main():
    """Run the example evaluation."""
    model = Model(name="gpt-4.1", benchmark=GSM8KBenchmark(), logfile_folder='examples/data')
    results = model.evaluate_on_benchmark()

    # You could save results to a file, send to a database, etc.
    print("\nEvaluation complete!")


if __name__ == "__main__":
    main()
