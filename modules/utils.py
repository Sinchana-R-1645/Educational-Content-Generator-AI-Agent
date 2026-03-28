import re

def clean_text(text):
    text = text.strip()
    text = re.sub(r'[^a-zA-Z0-9.,!? ]+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text
