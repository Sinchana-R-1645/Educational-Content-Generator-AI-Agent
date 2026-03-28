import streamlit as st
from modules.quiz import generate_quiz
from modules.flashcards import generate_flashcards
from modules.utils import clean_text
from modules.database import save_data, create_db, save_performance, get_last_performance

create_db()

st.title("📚 AI Study Assistant")

# Session state
if "answers" not in st.session_state:
    st.session_state.answers = {}

text = st.text_area("Enter study content:")

# Generate
if st.button("Generate"):

    if text.strip() == "":
        st.warning("Enter text")
    else:
        cleaned = clean_text(text)

        quiz = generate_quiz(cleaned)
        flashcards = generate_flashcards(cleaned)

        save_data(text, quiz, flashcards)

        st.session_state.quiz = quiz
        st.session_state.flashcards = flashcards
        st.session_state.answers = {}
        st.session_state.submitted = False

# ================= QUIZ =================
if "quiz" in st.session_state:

    st.subheader("📝 Quiz")

    for i, q in enumerate(st.session_state.quiz):

        st.write(f"Q{i+1}: {q['question']}")

        choice = st.radio(
            "Choose answer:",
            q["options"],
            key=f"q_{i}"
        )

        st.session_state.answers[i] = choice

    if st.button("Submit Quiz"):

        score = 0
        weak_areas = []

        for i, q in enumerate(st.session_state.quiz):

            if st.session_state.answers.get(i) == q["answer"]:
                score += 1
            else:
                weak_areas.append(q["context"])

        score = score / len(st.session_state.quiz)

        st.session_state.score = score
        st.session_state.weak_areas = weak_areas
        st.session_state.submitted = True

        save_performance(score, weak_areas)

# ================= RESULT =================
if st.session_state.get("submitted"):

    st.subheader("📊 Performance")

    score = st.session_state.score
    weak_areas = st.session_state.weak_areas

    st.write(f"Score: {round(score * 100)}%")

    if score < 0.5:
        st.error("You need revision ⚠️")
    else:
        st.success("Good job 🎉")

    st.subheader("✅ Correct Answers")
    for i, q in enumerate(st.session_state.quiz):
        st.write(f"Q{i+1}: {q['answer']}")

# ================= FLASHCARDS =================
if "flashcards" in st.session_state:

    st.subheader("🧠 Flashcards")

    for card in st.session_state.flashcards:
        with st.expander(card["front"]):
            st.write(card["back"])

# ================= REVISION =================
st.subheader("🔁 Smart Revision")

last_score, last_weak = get_last_performance()

if last_score is not None:

    st.write(f"Last Score: {round(last_score * 100)}%")

    if last_weak:
        st.write("Focus on these concepts:")

        for w in set(last_weak):
            st.info(w)

else:
    st.write("No previous performance found.")
