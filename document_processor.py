import PyPDF2
from docx import Document
import re
import wikipedia

def clean_text(text):

    text = text.replace("\\n", " ")

    text = re.sub(r'\\s+', ' ', text)

    return text

def read_pdf(file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return clean_text(text)

def read_docx(file):

    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    return clean_text(text)

def read_txt(file):

    text = file.read().decode("utf-8")

    return clean_text(text)

def get_topic_content(topic):

    try:

        content = wikipedia.summary(
            topic,
            sentences=8
        )

        return content

    except Exception as e:

        return f"Error fetching topic: {e}"
