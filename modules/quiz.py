import random

def generate_quiz(text):

    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]

    quiz = []

    stopwords = ["the", "is", "a", "an", "of", "in", "on", "and", "to"]

    for s in sentences[:5]:

        words = s.split()
        filtered_words = [w for w in words if w.lower() not in stopwords]

        if len(filtered_words) < 3:
            continue

        answer = random.choice(filtered_words)

        all_words = list(set(text.split()))
        wrong_options = random.sample(all_words, min(3, len(all_words)))

        options = list(set(wrong_options + [answer]))
        random.shuffle(options)

        question = f"In the sentence: '{s}', what does '{answer}' refer to?"

        quiz.append({
            "question": question,
            "options": options,
            "answer": answer,
            "context": s
        })

    if not quiz:
        quiz.append({
            "question": "What is the main topic?",
            "options": ["AI", "Data", "System", "Learning"],
            "answer": "AI",
            "context": text
        })

    return quiz
