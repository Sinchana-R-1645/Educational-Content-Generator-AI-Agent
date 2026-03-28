def generate_flashcards(text):

    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 15]

    flashcards = []

    for s in sentences[:5]:
        words = s.split()
        front = " ".join(words[:4]) + "..."
        back = s

        flashcards.append({
            "front": front,
            "back": back
        })

    return flashcards
