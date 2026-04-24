def generate_flashcards(text):
    sentences = [s.strip() for s in text.split('.') if len(s) > 10]
    cards = []

    for s in sentences[:6]:
        front = " ".join(s.split()[:3]) + "..."
        back = s
        cards.append((front, back))

    return cards
