from modules.quiz import generate_quiz
from modules.flashcards import generate_flashcards
from modules.utils import subjects_data
import streamlit as st
from PyPDF2 import PdfReader
import random

st.set_page_config(page_title="AI Study Assistant", layout="wide")

st.title("📚 AI Study Assistant")


# ---------- INPUT TYPE ----------
input_type = st.radio("Choose Input Method", ["Paste Text", "Select Subject", "Upload PDF"])

text = ""

# TEXT INPUT
if input_type == "Paste Text":
    text = st.text_area("Paste your study content here")

# SUBJECT INPUT
elif input_type == "Select Subject":
    st.write("### Click a Subject")

    if st.button("Physics"):
        st.session_state.text = subjects_data["Physics"]

    if st.button("ADA"):
        st.session_state.text = subjects_data["ADA"]

    if st.button("DBMS"):
        st.session_state.text = subjects_data["DBMS"]

    if st.button("Java"):
        st.session_state.text = subjects_data["Java"]

    text = st.session_state.get("text", "")

# PDF INPUT
elif input_type == "Upload PDF":
    file = st.file_uploader("Upload PDF", type=["pdf"])
    if file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""

# ---------- DIFFICULTY ----------
level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])


# ---------- SESSION ----------
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "cards" not in st.session_state:
    st.session_state.cards = []

# ---------- MAIN ----------
if text:
    st.success("Content Ready ✅")

    # QUIZ
    if st.button("Generate Quiz"):
        st.session_state.quiz = generate_quiz(text, level)

    if st.session_state.quiz:
        st.subheader("📝 Quiz")

        for i, (q, correct, opts) in enumerate(st.session_state.quiz):
            selected = st.radio(q, opts, key=f"q{i}")

            if st.button(f"Check Answer {i+1}", key=f"check{i}"):

                if selected == correct:
                    st.success("✅ Correct")
                else:
                    st.error("❌ Wrong")
                    st.write(f"✔ Correct Answer: {correct}")

                st.info(f"📘 Explanation: {correct}")

    # FLASHCARDS
    if st.button("Generate Flashcards"):
        st.session_state.cards = generate_flashcards(text)

    if st.session_state.cards:
        st.subheader("🧠 Flashcards")

        for i, (front, back) in enumerate(st.session_state.cards):
            if st.button(front, key=f"card{i}"):
                st.session_state[f"show{i}"] = True

            if st.session_state.get(f"show{i}", False):
                st.success(back)

else:
    st.info("Provide input to start")
           
