def generate_flashcards(questions, user_answers):

    flashcards = []

    for i, q in enumerate(questions):

        if user_answers[i] != q["answer"]:

            flashcards.append(
                {
                    "question": q["question"],
                    "answer": q["answer"]
                }
            )

    return flashcards
