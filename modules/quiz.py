from utils import llm
import json

def generate_quiz(text, level, qtype):

    if qtype == "MCQ":
        prompt = f"""
Create 5 MCQ questions.

Format STRICT JSON like this:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Difficulty: {level}

Content:
{text}
"""
    else:
        prompt = f"""
Create 5 {qtype} questions.

Return JSON format:
[
  {{
    "question": "...",
    "answer": "..."
  }}
]

Content:
{text}
"""

    return llm(prompt)
