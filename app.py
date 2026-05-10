import streamlit as st

from document_processor import (
    read_pdf,
    read_docx,
    read_txt,
    get_topic_content
)

from quiz import (
    generate_ai_quiz
)

from flashcards import (
    generate_flashcards
)

from audio_generator import (
    generate_audio
)

from analysis import (
    generate_chart
)

from export_utils import (
    export_quiz_pdf,
    export_flashcards
)

from database import (
    save_score,
    get_scores
)

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="LearnGenie : AI Educational Tutor",
    layout="wide"
)

st.title("📚 AI Educational Content Generator")

# ---------------------------------------
# SIDEBAR MENU
# ---------------------------------------

menu = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Upload Content",
        "Quiz",
        "Flashcards",
        "Audio Summary",
        "Dashboard"
    ]
)

# ---------------------------------------
# SESSION STATE
# ---------------------------------------

if "content" not in st.session_state:
    st.session_state.content = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

# ---------------------------------------
# UPLOAD CONTENT
# ---------------------------------------

if menu == "Upload Content":

    st.header("📄 Upload Study Material")

    uploaded_file = st.file_uploader(
        "Upload PDF / TXT / DOCX",
        type=["pdf", "txt", "docx"]
    )

    st.subheader("OR Enter Content")

    topic = st.text_input(
        "Enter Study Topic"
    )

    manual_text = st.text_area(
        "Paste Study Notes"
    )

    if uploaded_file:

        try:

            file_type = uploaded_file.name.split(".")[-1].lower()

            if file_type == "pdf":

                text = read_pdf(uploaded_file)

            elif file_type == "docx":

                text = read_docx(uploaded_file)

            else:

                text = read_txt(uploaded_file)

            if text.strip() == "":

                st.error("No text found in document")

            else:

                st.session_state.content = text

                st.success("✅ File Processed Successfully")

                st.text_area(
                    "Extracted Content",
                    text,
                    height=300
                )

        except Exception as e:

            st.error(f"Error processing file: {e}")

    elif manual_text.strip() != "":

        st.session_state.content = manual_text

        st.success("✅ Manual Notes Added")

        st.text_area(
            "Study Content",
            manual_text,
            height=300
        )

    elif topic.strip() != "":

        try:

            text = get_topic_content(topic)

            st.session_state.content = text

            st.success("✅ Topic Content Loaded")

            st.text_area(
                "Study Content",
                text,
                height=300
            )

        except Exception as e:

            st.error(f"Topic fetch failed: {e}")

# ---------------------------------------
# QUIZ SECTION
# ---------------------------------------

elif menu == "Quiz":

    st.header("🧠 Quiz Creation & Taking")

    if st.session_state.content == "":

        st.warning("Please upload study material first")

    else:

        difficulty = st.selectbox(
            "Select Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        quiz_type = st.selectbox(
            "Quiz Type",
            [
                "MCQ",
                "True/False",
                "Conceptual",
                "Application Based"
            ]
        )

        if st.button("Generate Quiz"):

            try:

                with st.spinner("Generating AI Quiz..."):

                    st.session_state.questions = generate_ai_quiz(
                        st.session_state.content,
                        difficulty,
                        quiz_type
                    )

                st.success("Quiz Generated Successfully")

            except Exception as e:

                st.error(f"Quiz generation failed: {e}")

        if st.session_state.questions:

            user_answers = []

            score = 0

            for i, q in enumerate(st.session_state.questions):

                st.subheader(f"Question {i+1}")

                answer = st.radio(
                    q["question"],
                    q["options"],
                    key=f"quiz_{i}"
                )

                user_answers.append(answer)

            if st.button("Submit Quiz"):

                for i, q in enumerate(st.session_state.questions):

                    if user_answers[i] == q["answer"]:

                        score += 1

                st.success(
                    f"🎯 Your Score: {score}/{len(st.session_state.questions)}"
                )

                accuracy = (
                    score / len(st.session_state.questions)
                ) * 100

                st.metric(
                    "Accuracy",
                    f"{accuracy:.2f}%"
                )

                save_score(
                    "General",
                    score,
                    len(st.session_state.questions)
                )

                st.session_state.flashcards = generate_flashcards(
                    st.session_state.questions,
                    user_answers
                )

                st.info(
                    "Flashcards generated from incorrect answers"
                )

                try:

                    quiz_pdf = export_quiz_pdf(
                        st.session_state.questions
                    )

                    with open(quiz_pdf, "rb") as file:

                        st.download_button(
                            label="⬇ Download Quiz PDF",
                            data=file,
                            file_name="quiz.pdf",
                            mime="application/pdf"
                        )

                except Exception as e:

                    st.error(f"Quiz PDF export failed: {e}")

                try:

                    flashcard_pdf = export_flashcards(
                        st.session_state.flashcards
                    )

                    with open(flashcard_pdf, "rb") as file:

                        st.download_button(
                            label="⬇ Download Flashcards PDF",
                            data=file,
                            file_name="flashcards.pdf",
                            mime="application/pdf"
                        )

                except Exception as e:

                    st.error(f"Flashcard PDF export failed: {e}")

# ---------------------------------------
# FLASHCARDS
# ---------------------------------------

elif menu == "Flashcards":

    st.header("📘 Flashcard Review System")

    if len(st.session_state.flashcards) == 0:

        st.warning(
            "Complete the quiz first to generate flashcards"
        )

    else:

        flashcards = st.session_state.flashcards

        for i, card in enumerate(flashcards):

            with st.expander(f"Flashcard {i+1}"):

                st.write("### Question")

                st.write(card["question"])

                show = st.button(
                    f"Show Answer {i+1}",
                    key=f"show_{i}"
                )

                if show:

                    st.write("### Answer")

                    st.success(card["answer"])

                    understood = st.radio(
                        "Did you understand?",
                        ["Yes", "No"],
                        key=f"review_{i}"
                    )

                    if understood == "No":

                        st.warning(
                            "This flashcard will appear again for revision"
                        )

# ---------------------------------------
# AUDIO SUMMARY
# ---------------------------------------

elif menu == "Audio Summary":

    st.header("🔊 Audio Summary")

    if st.session_state.content == "":

        st.warning("Please upload content first")

    else:

        if st.button("Generate Audio"):

            try:

                summary = st.session_state.content[:500]

                path = generate_audio(summary)

                audio_file = open(path, "rb")

                st.audio(audio_file.read())

                st.success("Audio Generated Successfully")

            except Exception as e:

                st.error(f"Audio generation failed: {e}")

# ---------------------------------------
# DASHBOARD
# ---------------------------------------

elif menu == "Dashboard":

    st.header("📊 Study Dashboard")

    scores = get_scores()

    st.metric(
        "Total Quiz Attempts",
        len(scores)
    )

    fig = generate_chart()

    if fig:

        st.pyplot(fig)

    else:

        st.info("No Quiz Attempts Yet")
