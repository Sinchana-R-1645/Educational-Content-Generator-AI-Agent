import json
import streamlit as st
from quiz import generate_quiz

# session storage
if "score" not in st.session_state:
    st.session_state.score = 0

if content:

    if st.button("Generate Quiz"):

        raw = generate_quiz(content, level, qtype)

        try:
            quiz_data = json.loads(raw)
        except:
            st.error("Error generating quiz format")
            st.stop()

        st.session_state.quiz = quiz_data
        st.session_state.answers = {}

    # SHOW QUIZ
    if "quiz" in st.session_state:

        st.subheader("📝 Quiz")

        for i, q in enumerate(st.session_state.quiz):

            st.write(q["question"])

            if qtype == "MCQ":
                st.session_state.answers[i] = st.radio(
                    f"Q{i+1}",
                    q["options"],
                    key=i
                )
            else:
                st.session_state.answers[i] = st.text_input(
                    f"Answer {i+1}",
                    key=i
                )

        if st.button("Submit Quiz"):

            score = 0

            for i, q in enumerate(st.session_state.quiz):

                if st.session_state.answers[i].strip().lower() == q["answer"].strip().lower():
                    score += 1

            st.session_state.score += score

            st.success(f"Score: {score}/5")
            st.info(f"Total Progress Score: {st.session_state.score}")
