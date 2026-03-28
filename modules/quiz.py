import random
import re

def generate_quiz(text):

    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 25]

    quiz = []

    for s in sentences[:5]:

        words = s.split()

        # Better keyword filtering
        stopwords = {"this","that","which","their","there","about","would","could","should","because"}
        keywords = [w for w in words if len(w) > 4 and w.lower() not in stopwords]

        if not keywords:
            continue

        answer = keywords[0]   # stable choice

        # Replace only first occurrence
        blank_sentence = s.replace(answer, "_____", 1)

        # Better wrong options
        all_words = list(set(text.split()))
        wrong_options = [w for w in all_words if w != answer and len(w) > 4]

        wrong_choices = random.sample(wrong_options, min(3, len(wrong_options)))

        options = wrong_choices + [answer]
        random.shuffle(options)

        question = f"Fill in the blank:\n\n{blank_sentence}"

        quiz.append({
            "question": question,
            "options": options,
            "answer": answer,
            "context": s
        })

    if not quiz:
        quiz.append({
            "question": "What is the main topic?",
            "options": ["Science", "Technology", "Education", "General Knowledge"],
            "answer": "General Knowledge",
            "context": text
        })

    return quiz
