import re

def generate_flashcards(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 20]

    cards = []

    for s in sentences[:5]:
        words = s.split()
        concept = " ".join(words[:3])

        cards.append({
            "front": concept,
            "back": s
        })

    return cards
