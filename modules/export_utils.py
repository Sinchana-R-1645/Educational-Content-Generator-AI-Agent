from fpdf import FPDF

def export_quiz_pdf(questions):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(
        200,
        10,
        txt="Quiz Questions",
        ln=True
    )

    for i, q in enumerate(questions):

        pdf.multi_cell(
            0,
            10,
            txt=f"{i+1}. {q['question']}"
        )

    path = "quiz.pdf"

    pdf.output(path)

    return path

def export_flashcards(flashcards):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(
        200,
        10,
        txt="Flashcards",
        ln=True
    )

    for i, card in enumerate(flashcards):

        pdf.multi_cell(
            0,
            10,
            txt=f"""
Question:
{card['question']}

Answer:
{card['answer']}
"""
        )

    path = "flashcards.pdf"

    pdf.output(path)

    return path
