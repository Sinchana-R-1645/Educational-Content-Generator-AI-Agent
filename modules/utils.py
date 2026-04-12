from groq import Groq
import os
import pdfplumber
import docx

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

def llm(prompt):
    return client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}]
    ).choices[0].message.content


def read_file(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for p in pdf.pages:
                text += p.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return file.read().decode("utf-8")
