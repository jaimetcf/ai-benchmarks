import os
from openai import OpenAI
#from openai.types.chat import FunctionDefinition
import json
from typing import Any

MODEL = "gpt-4.1"

functions: list[Any] = [
    {
        "name": "compare_code",
        "description": "Compare two code snippets and determine if they produce the same output.",
        "parameters": {
            "type": "object",
            "properties": {
                "sameResult": {"type": "boolean"},
                "reason": {"type": "string"}
            },
            "required": ["sameResult", "reason"]
        }
    }
]


class CodeComparer:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.client = OpenAI(api_key=api_key)

    def compare(self, code1: str, code2: str, code_type: str) -> dict:
        user_prompt = (
            f"Compare these two {'code snippets' if code_type == 'Python code' else 'terminal commands'}:\n"
            f"Code1: {code1}\n"
            f"Code2: {code2}\n"
            "Determine if they produce the same output."
        )
        
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            tools=[{    # This ensures the response is a valid JSON object
                "type": "function",
                "function": {
                    "name": "compare_code",
                    "description": "Compare two code snippets and determine if they produce the same output.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sameResult": {"type": "boolean"},
                            "reason": {"type": "string"}
                        },
                        "required": ["sameResult", "reason"]
                    }
                }
            }],
            tool_choice={"type": "function", "function": {"name": "compare_code"}},
            temperature=0
        )
        
        # Extract the function call arguments
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls is None or len(tool_calls) == 0:
            return {"sameResult": None, "reason": "No function call returned"}
        
        tool_call = tool_calls[0]
        return json.loads(tool_call.function.arguments)
