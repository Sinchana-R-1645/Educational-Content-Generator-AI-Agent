import re

def generate_flashcards(text):

    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.strip()) > 25]

    flashcards = []

    for s in sentences[:5]:

        if " is " in s:
            parts = s.split(" is ", 1)
            front = parts[0].strip()
            back = parts[1].strip()
        else:
            words = s.split()
            front = " ".join(words[:6]) + "..."
            back = s

        flashcards.append({
            "front": front,
            "back": back
        })

    return flashcards
