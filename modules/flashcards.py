
from utils import llm

def generate_flashcards(text):
    prompt = f"""
Create 5 flashcards.

Format:
Q: ...
A: ...

{text[:2000]}
"""
    result = llm(prompt)

    cards = []
    parts = result.split("Q:")

    for part in parts[1:]:
        if "A:" in part:
            q, a = part.split("A:",1)
            cards.append((q.strip(), a.strip()))

    return cards
