from utils import llm

def generate_quiz(text, level, qtype):

    prompt = f"""
You are a teacher.

Create a {level} difficulty {qtype} quiz.

Content:
{text}

Rules:
- MCQ: 4 options + answer
- True/False: statement + answer
- Fill blanks: sentence + answer
"""

    return llm(prompt)
