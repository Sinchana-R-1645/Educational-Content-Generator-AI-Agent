import json

from utils import (
    llm,
    clean_json
)

def generate_ai_quiz(
    text,
    difficulty,
    quiz_type
):

    prompt = f"""
Generate 5 quiz questions.

Difficulty Level:
{difficulty}

Quiz Type:
{quiz_type}

Return ONLY valid JSON.

Format:

[
 {{
   "question": "",
   "options": ["", "", "", ""],
   "answer": ""
 }}
]

Content:
{text[:3000]}
"""

    try:

        response = llm(prompt)

        cleaned = clean_json(response)

        questions = json.loads(cleaned)

        return questions

    except Exception as e:

        print(e)

        return []
