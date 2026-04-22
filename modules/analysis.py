from utils import llm

def summarize_text(text):
    prompt = f"Summarize this in easy points:\n{text}"
    return llm(prompt)

def extract_topics(text):
    prompt = f"Give only main topics from this content as bullet points:\n{text}"
    return llm(prompt)
