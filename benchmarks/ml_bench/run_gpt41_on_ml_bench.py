"""
- This script is used to generate the answers for the GPT-4.1 model on the ML-Bench benchmark 
test dataset (all 260 questions, or a subset of it).
- The answers are saved to a file in the data/ml_bench_gpt-4.1_answers.jsonl file.
- It uses the OpenAI API to run the model.
- Before running this script, you need to set the OPENAI_API_KEY environment variable with a valid OpenAI API key.
"""
try:
    from openai import OpenAI
except ImportError:
    raise ImportError("The OpenAI Python SDK v1.x is required. Install with: pip install --upgrade openai")

import os
import json
import time
from typing import Any
from tqdm import tqdm

# Path setup
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'test.jsonl')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ml_bench_gpt-4.1_answers.jsonl')

# OpenAI API setup
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it to your OpenAI API key.")
client = OpenAI(api_key=api_key)
MODEL = "gpt-4.1"

# System prompt to ensure the model appends the required string

# Read all questions from the input file
tasks = []
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        tasks.append(item)

# Randomly select 30 questions with a fixed seed for reproducibility
import random
random.seed(42)
# Get 260 unique random indices from the original questions list
sampled_indices = random.sample(range(len(tasks)), 260)

sys_prompt = (
    "Your response will always be only the python code or the terminal command that will execute the instruction in the prompt.\n"
    "Don't add any other information or any additional word in the response beyonds the code\n"
)

results = []
for idx in tqdm(sampled_indices, desc="Processing questions"):
    task = tasks[idx]
    user_prompt = (
        f"For executing the instruction below in this prompt, you will consult the code in the following github file {task["github"]}/{task["path"]}\n"
        f"The arguments for the script are: {task["arguments"]}\n"
        f"The instruction is: {task["instruction"]}\n"
    )
    messages: Any = [
        {"role": "system", "content": sys_prompt}, 
        {"role": "user", "content": user_prompt}
    ]    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.0,
            max_tokens=512,
        )
        answer = (response.choices[0].message.content or "").strip()

    except Exception as e:
        answer = f"[ERROR] {e}"
    # Save the result in a similar structure used in test.jsonl file
    results.append({"question_id": f"{idx:04d}", "question": user_prompt, "answer": answer})

    # Delay to respect RPM (e.g., 1 seconds per request for ~60 RPM)
    time.sleep(1)

# Write results to output file
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    for item in results:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Done! Saved {len(results)} answers to {OUTPUT_PATH}")
