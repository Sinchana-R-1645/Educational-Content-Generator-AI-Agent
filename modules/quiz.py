from utils import llm
import json
import re

def clean_json(text):
    text = text.replace("```json", "").replace("```", "").strip()
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return match.group(0)
    return text

def generate_quiz(text, level, qtype):
    if qtype == "MCQ":
        format_text = """
[
  {
    "question":"What is Python?",
    "options":["Snake","Programming Language","Game","Browser"],
    "answer":"Programming Language"
  }
]
"""
    elif qtype == "True/False":
        format_text = """
[
  {
    "question":"Python is a programming language.",
    "options":["True","False"],
    "answer":"True"
  }
]
"""
    else:
        format_text = """
[
  {
    "question":"Python is a _____ language.",
    "answer":"programming"
  }
]
"""

    prompt = f"""
Generate exactly 5 {qtype} quiz questions.

Difficulty: {level}

Return ONLY a valid JSON array.
Do not write explanations.
Do not use markdown.

Format example:
{format_text}

Content:
{text[:3000]}
"""

    try:
        result = llm(prompt)
        cleaned = clean_json(result)
        data = json.loads(cleaned)

        if isinstance(data, list) and len(data) > 0:
            return data
        else:
            return []

    except Exception as e:
        print("Quiz Error:", e)
        return []
