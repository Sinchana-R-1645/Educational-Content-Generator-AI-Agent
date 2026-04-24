import streamlit as st
from modules.quiz import generate_quiz
from modules.flashcards import generate_flashcards
from modules.utils import read_file, generate_audio
from modules.analysis import summarize_text, extract_topics

st.set_page_config(page_title="AI Study Agent", page_icon="📚", layout="wide")

st.title("📚 AI Educational Agent")

# Session state
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "index" not in st.session_state:
    st.session_state.index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "qtype" not in st.session_state:
    st.session_state.qtype = "MCQ"
if "cards" not in st.session_state:
    st.session_state.cards = []

# Input
file = st.file_uploader("Upload file", type=["pdf", "txt"])
topic = st.text_input("Or enter topic")

content = ""
if file:
    content = read_file(file)
elif topic:
    content = topic

level = st.selectbox("Difficulty", ["easy", "medium", "hard"])
qtype = st.selectbox("Quiz Type", ["MCQ", "True/False", "Fill in the blanks"])

# Tools
if st.button("Summary"):
    if content:
        st.write(summarize_text(content))

if st.button("Topics"):
    if content:
        st.write(extract_topics(content))

if st.button("Audio"):
    if content:
        path = generate_audio(content)
        st.audio(path)

# Generate Quiz
if st.button("Generate Quiz"):
    if content:
        st.session_state.quiz = generate_quiz(content, level, qtype)
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.qtype = qtype

# Quiz
if st.session_state.quiz:
    q = st.session_state.quiz[st.session_state.index]

    st.subheader(q["question"])

    if st.session_state.qtype in ["MCQ", "True/False"]:
        ans = st.radio("Choose", q["options"])
    else:
        ans = st.text_input("Answer")

    if st.button("Submit") and not st.session_state.submitted:
        st.session_state.submitted = True
        if ans.lower() == q["answer"].lower():
            st.success("Correct")
            st.session_state.score += 1
        else:
            st.error(f"Wrong: {q['answer']}")

    if st.session_state.submitted:
        if st.button("Next"):
            st.session_state.index += 1
            st.session_state.submitted = False

# Flashcards
if st.button("Generate Flashcards"):
    if content:
        st.session_state.cards = generate_flashcards(content)

if st.session_state.cards:
    for q, a in st.session_state.cards:
        with st.expander(q):
            st.write(a)
