
import json, re
from utils import llm

def clean(text):
    text = text.replace("```json","").replace("```","")
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return match.group(0) if match else text

def generate_quiz(text, level):
    prompt = f"""
Generate exactly 5 MCQ questions.

Difficulty: {level}

Return JSON:
[
{{"question":"","options":["","","",""],"answer":""}}
]

{text[:2000]}
"""
    try:
        return json.loads(clean(llm(prompt)))
    except:
        return []
