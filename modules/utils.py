%%writefile utils.py
import os
from groq import Groq
import wikipedia
import pdfplumber
import docx
from gtts import gTTS

def get_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return None
    return Groq(api_key=key)

def llm(prompt):
    try:
        client = get_client()
        if not client:
            return "⚠️ Missing GROQ API key"
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":prompt}],
            temperature=0.3
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"LLM error: {str(e)}"

# 🔥 FILE READER (PDF / DOCX / TXT)
def read_file(file):
    try:
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

    except:
        return ""

# 🔥 SMART CONTENT
def get_content(topic):
    try:
        text = wikipedia.summary(topic, sentences=5)
        if text:
            return "📘 Wikipedia:\n\n" + text
    except:
        pass

    return llm(f"Explain this topic clearly:\n{topic}")

def generate_audio(text):
    try:
        tts = gTTS(text=text[:2000])
        tts.save("audio.mp3")
        return "audio.mp3"
    except:
        return None



# 🎤 VOICE INPUT
import speech_recognition as sr

def voice_to_text():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source, timeout=5)

        text = r.recognize_google(audio)
        return text
    except:
        return "Voice input failed"


# 📄 PDF EXPORT
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(text):
    file = "study_notes.pdf"
    doc = SimpleDocTemplate(file)
    styles = getSampleStyleSheet()

    content = [Paragraph(text, styles["Normal"])]

    doc.build(content)
    return file
