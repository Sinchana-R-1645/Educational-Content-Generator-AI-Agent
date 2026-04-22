from groq import Groq
import os
import pdfplumber
import docx
from gtts import gTTS

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

def llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def read_file(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return file.read().decode("utf-8")

def generate_audio(text):
    tts = gTTS(text=text[:3000], lang='en')
    tts.save("summary.mp3")
    return "summary.mp3"
