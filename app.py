import streamlit as st
from quiz import generate_quiz
from flashcards import generate_flashcards
from utils import read_file

st.title("📚 AI Educational Agent")

file = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf","docx","txt"])
topic = st.text_input("OR Enter Topic")

content = ""

if file:
    content = read_file(file)
elif topic:
    content = topic

if content:

    level = st.selectbox("Difficulty", ["easy", "medium", "hard"])
    qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Fill in blanks"])

    if st.button("Generate Quiz"):
        st.write(generate_quiz(content, level, qtype))

    if st.button("Generate Flashcards"):
        st.write(generate_flashcards(content))
