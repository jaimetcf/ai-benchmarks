"""
- This script is used to generate the answers for the GPT-4.1 model on the GSM8K benchmark 
test dataset (all 1319 questions, or a random subset of it).
- The answers are saved to a file in the data/gsm8k_gpt-4.1_answers.jsonl file.
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
from tqdm import tqdm

# Path setup
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'test.jsonl')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'data', 'gsm8k_gpt-4.1_answers.jsonl')

# OpenAI API setup
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it to your OpenAI API key.")
client = OpenAI(api_key=api_key)
MODEL = "gpt-4.1"

# System prompt to ensure the model appends the required string
SYSTEM_PROMPT = (
    "You are a math problem solver. For every question, answer as concisely as possible, "
    "and at the end of your answer, append a newline and '#### <response number>' where <response number> is your final answer. "
    "For example, if the answer is 42, end your response with '\n#### 42'. Do not add any other text after this line."
)

# Read all questions from the input file
questions = []
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        item = json.loads(line)
        questions.append(item)

# Randomly select 30 questions with a fixed seed for reproducibility
import random
random.seed(42)
# Get 30 unique random indices from the original questions list
sampled_indices = random.sample(range(len(questions)), 1319)

results = []
for idx in tqdm(sampled_indices, desc="Processing questions"):
    item = questions[idx]
    question = item["question"]
    # Prepare messages for OpenAI API
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
    # Call the API
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
    results.append({"question_id": f"{idx:04d}", "question": question, "answer": answer})

    # Delay to respect RPM (e.g., 1 seconds per request for ~60 RPM)
    time.sleep(2)

# Write results to output file
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    for item in results:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Done! Saved {len(results)} answers to {OUTPUT_PATH}")
