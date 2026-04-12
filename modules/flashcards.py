from utils import llm

def generate_flashcards(text):

    prompt = f"""
Create 5 flashcards.

Format:
Q: question
A: answer

Content:
{text}
"""

    result = llm(prompt)

    # convert into proper flashcard UI
    cards = result.split("Q:")

    output = ""

    for c in cards[1:]:
        if "A:" in c:
            q, a = c.split("A:")
            output += f"❓ {q.strip()}\n💡 {a.strip()}\n\n"

    return output
