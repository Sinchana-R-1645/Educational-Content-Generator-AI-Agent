%%writefile app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.utils import get_content, llm, generate_audio, read_file, voice_to_text, export_pdf
from modules.quiz import generate_quiz
from modules.flashcards import generate_flashcards
from modules.database import save, get

st.set_page_config(layout="wide")
st.title("📚LearnGenie - AI Study Assistant")

menu = st.sidebar.radio("Menu", ["Study","Quiz","Flashcards","Analytics","Audio"])

# ---------- SESSION ----------
if "content" not in st.session_state:
    st.session_state.content = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "cards" not in st.session_state:
    st.session_state.cards = []

# ---------- STUDY ----------
if menu == "Study":

    st.subheader("📥 Input Content")

    # 🎤 Voice Input
    if st.button("🎤 Speak Topic"):
        spoken = voice_to_text()
        st.write("You said:", spoken)
        st.session_state.content = get_content(spoken)

    # Other Inputs
    file = st.file_uploader("Upload PDF / DOCX / TXT", type=["pdf","docx","txt"])
    topic = st.text_input("OR Enter Topic")
    text_input = st.text_area("OR Paste Text")

    if st.button("Load Content"):

        if file:
            st.session_state.content = read_file(file)

        elif text_input.strip():
            st.session_state.content = text_input

        elif topic.strip():
            st.session_state.content = get_content(topic)

        else:
            st.warning("Provide some input")

    # Show content
    if st.session_state.content:

        st.success("Content Loaded ✅")
        st.write(st.session_state.content[:1500])

        # 📄 Export PDF
        if st.button("📄 Export Notes as PDF"):
            file_path = export_pdf(st.session_state.content)
            with open(file_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="notes.pdf")

        # 🧠 Summary
        if st.button("Generate Summary"):
            st.write(llm("Summarize:\n" + st.session_state.content))

# ---------- QUIZ ----------
elif menu == "Quiz":

    level = st.selectbox("Difficulty", ["easy","medium","hard"])

    if not st.session_state.content:
        st.warning("Go to Study first")
    else:
        if st.button("Generate Quiz"):
            st.session_state.quiz = generate_quiz(st.session_state.content, level)
            st.session_state.score = 0

        if st.session_state.quiz:
            for i, q in enumerate(st.session_state.quiz):

                ans = st.radio(q["question"], q["options"], key=f"q{i}")

                if st.button(f"Check {i+1}", key=f"btn{i}"):
                    if ans == q["answer"]:
                        st.success("Correct ✅")
                        st.session_state.score += 1
                    else:
                        st.error(f"Wrong ❌ → {q['answer']}")

            if st.button("Finish Quiz"):
                total = len(st.session_state.quiz)
                score = st.session_state.score

                st.success(f"Score: {score}/{total}")
                save("topic", score, total)

                percent = (score / total) * 100

                if percent >= 70:
                    st.success("🔥 Next Level: HARD")
                elif percent >= 40:
                    st.warning("⚡ Next Level: MEDIUM")
                else:
                    st.info("📘 Next Level: EASY")

# ---------- FLASHCARDS ----------
elif menu == "Flashcards":

    if not st.session_state.content:
        st.warning("Add content first")
    else:
        if st.button("Generate Flashcards"):
            st.session_state.cards = generate_flashcards(st.session_state.content)

        if st.session_state.cards:
            for i, (q, a) in enumerate(st.session_state.cards):
                with st.expander(f"Card {i+1}: {q}"):
                    st.write(a)

# ---------- ANALYTICS ----------
elif menu == "Analytics":
    show_analysis()
# ---------- AUDIO ----------
elif menu == "Audio":

    if st.session_state.content:
        if st.button("Generate Audio"):
            file = generate_audio(st.session_state.content)
            if file:
                st.audio(open(file, "rb").read())
    else:
        st.warning("Add content first")
