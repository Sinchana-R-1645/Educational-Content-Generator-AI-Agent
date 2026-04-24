import random
def generate_quiz(text, level):
    sentences = [s.strip() for s in text.split('.') if len(s) > 15]
    quiz = []

    for i in range(min(5, len(sentences))):
        correct = sentences[i]

        if level == "Easy":
            question = f"What is: {correct}?"
        elif level == "Medium":
            question = f"Identify correct statement: {correct[:30]}..."
        else:
            question = f"Which best explains: {correct[:25]}...?"

        options = random.sample(sentences, min(4, len(sentences)))
        if correct not in options:
            options[0] = correct

        random.shuffle(options)
        quiz.append((question, correct, options))

    return quiz
