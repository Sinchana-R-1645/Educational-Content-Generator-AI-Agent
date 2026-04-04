import random
import re

def generate_quiz(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 25]

    quiz = []

    for s in sentences[:5]:

        words = s.split()
        keywords = [w for w in words if len(w) > 5]

        if not keywords:
            continue

        answer = random.choice(keywords)

        all_words = list(set(text.split()))
        wrong = [w for w in all_words if w != answer and len(w) > 4]

        wrong_options = random.sample(wrong, min(3, len(wrong)))
        options = wrong_options + [answer]
        random.shuffle(options)

        # MCQ
        quiz.append({
            "type": "mcq",
            "question": f"What word best fits the sentence?\n\n{s}",
            "options": options,
            "answer": answer,
            "context": s
        })

        # True/False
        tf_statement = s.replace(answer, random.choice(wrong) if wrong else answer)
        quiz.append({
            "type": "true_false",
            "question": f"True or False:\n\n{tf_statement}",
            "options": ["True", "False"],
            "answer": "False",
            "context": s
        })

        # Fill in the blank
        blank = s.replace(answer, "_____")
        quiz.append({
            "type": "fill_blank",
            "question": f"Fill in the blank:\n\n{blank}",
            "options": options,
            "answer": answer,
            "context": s
        })

    # fallback
    if not quiz:
        quiz.append({
            "type": "mcq",
            "question": "What is the main topic?",
            "options": ["Science", "Technology", "Education", "General Knowledge"],
            "answer": "General Knowledge",
            "context": text
        })

    return quiz
