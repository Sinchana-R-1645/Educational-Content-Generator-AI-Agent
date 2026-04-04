import streamlit as st
import PyPDF2

from modules.quiz import generate_quiz
from modules.flashcards import generate_flashcards
from modules.utils import clean_text
from modules.database import (
    save_data, create_db, save_performance,
    get_last_performance, get_stats
)

create_db()

st.set_page_config(page_title="AI Study Assistant", layout="wide")
st.title("📚 AI Study Assistant")

tabs = st.tabs(["📄 Input", "📝 Quiz", "🧠 Flashcards", "📊 Progress"])

# ================= INPUT =================
with tabs[0]:
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    text = st.text_area("Or enter study content:")

    if st.button("Generate"):
        try:
            if uploaded_file:
                if uploaded_file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(uploaded_file)
                    text = " ".join([page.extract_text() or "" for page in reader.pages])
                else:
                    text = uploaded_file.read().decode("utf-8")

            if not text.strip():
                st.warning("Please provide input")
            else:
                cleaned = clean_text(text)

                quiz = generate_quiz(cleaned)
                flashcards = generate_flashcards(cleaned)

                save_data(text, quiz, flashcards)

                st.session_state.quiz = quiz
                st.session_state.flashcards = flashcards
                st.session_state.answers = {}

                st.success("✅ Content processed successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ================= QUIZ =================
with tabs[1]:
    if "quiz" in st.session_state:

        score = 0
        total = len(st.session_state.quiz)

        for i, q in enumerate(st.session_state.quiz):
            st.write(f"**Q{i+1}: {q['question']}**")

            choice = st.radio(
                "Choose answer:",
                q["options"],
                key=f"q_{i}"
            )

            st.session_state.answers[i] = choice

        if st.button("Submit Quiz"):
            weak = []

            for i, q in enumerate(st.session_state.quiz):
                if st.session_state.answers.get(i) == q["answer"]:
                    score += 1
                else:
                    weak.append(q["context"])

            final_score = score / total
            save_performance(final_score, weak)

            st.subheader("📊 Results")
            st.success(f"Score: {round(final_score * 100)}%")

            if final_score < 0.5:
                st.error("⚠️ You need revision")
            else:
                st.success("🎉 Good job!")

# ================= FLASHCARDS =================
with tabs[2]:
    if "flashcards" in st.session_state:
        for card in st.session_state.flashcards:
            with st.expander(card["front"]):
                st.write(card["back"])

# ================= PROGRESS =================
with tabs[3]:
    total, avg = get_stats()
    last_score, last_weak = get_last_performance()

    st.subheader("📈 Your Progress")
    st.write(f"Total Attempts: {total}")
    st.write(f"Average Score: {avg * 100}%")

    if last_score:
        st.write(f"Last Score: {round(last_score * 100)}%")

        if last_weak:
            st.write("🔁 Focus on:")
            for w in set(last_weak):
                st.info(w)
    else:
        st.write("No attempts yet.")
