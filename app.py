import streamlit as st
from quiz import generate_quiz
from flashcards import generate_flashcards
from utils import read_file, generate_audio
from analysis import summarize_text, extract_topics

st.set_page_config(page_title="AI Study Agent", page_icon="📚", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}
h1,h2,h3 {
    color:white;
}
.stButton>button {
    width:100%;
    border-radius:12px;
    padding:10px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Educational Agent")
st.caption("Smart Quiz • Flashcards • Summary • Audio Learning")

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
file = st.file_uploader("📂 Upload PDF / DOCX / TXT", type=["pdf", "docx", "txt"])
topic = st.text_input("OR Enter Topic")

content = ""
if file:
    content = read_file(file)
elif topic:
    content = topic

level = st.selectbox("🎯 Difficulty", ["easy", "medium", "hard"])
qtype = st.selectbox("📝 Quiz Type", ["MCQ", "True/False", "Fill in the blanks"])

# Tools
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Summary"):
        if content.strip():
            st.write(summarize_text(content))
        else:
            st.warning("Enter content first")

with col2:
    if st.button("🧠 Topics"):
        if content.strip():
            st.write(extract_topics(content))
        else:
            st.warning("Enter content first")

with col3:
    if st.button("🔊 Audio"):
        if content.strip():
            path = generate_audio(content)
            st.audio(open(path, "rb").read())
        else:
            st.warning("Enter content first")

st.markdown("---")

# Generate Quiz
if st.button("🎯 Generate Quiz"):
    if content.strip():
        quiz_data = generate_quiz(content, level, qtype)
        if quiz_data:
            st.session_state.quiz = quiz_data
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.submitted = False
            st.session_state.qtype = qtype
        else:
            st.error("Quiz generation failed")
    else:
        st.warning("Enter content first")

# Quiz
if st.session_state.quiz:
    total = len(st.session_state.quiz)
    st.write(f"Score: {st.session_state.score}/{total}")

    if st.session_state.index < total:
        q = st.session_state.quiz[st.session_state.index]
        st.subheader(q["question"])

        if st.session_state.qtype in ["MCQ", "True/False"]:
            ans = st.radio("Select:", q["options"])
        else:
            ans = st.text_input("Answer:")

        if st.button("Submit") and not st.session_state.submitted:
            st.session_state.submitted = True
            if ans.strip().lower() == q["answer"].strip().lower():
                st.success("Correct")
                st.session_state.score += 1
            else:
                st.error(f"Wrong. Answer: {q['answer']}")

        if st.session_state.submitted:
            if st.button("Next"):
                st.session_state.index += 1
                st.session_state.submitted = False
    else:
        st.success(f"Final Score: {st.session_state.score}/{total}")

# Flashcards
st.markdown("---")
st.subheader("Flashcards")

if st.button("Generate Flashcards"):
    if content.strip():
        st.session_state.cards = generate_flashcards(content)
    else:
        st.warning("Enter content first")

if st.session_state.cards:
    for i, (q, a) in enumerate(st.session_state.cards, 1):
        with st.expander(f"{q}"):
            st.write(a)

# Voice
st.markdown("---")
st.text_input("🎤 Speak your question:")
