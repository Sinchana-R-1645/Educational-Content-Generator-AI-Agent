import sqlite3

conn = sqlite3.connect("study.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scores(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    score INTEGER,
    total INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS flashcards(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
)
""")

conn.commit()

def save_score(subject, score, total):

    cursor.execute(
        "INSERT INTO scores(subject, score, total) VALUES(?,?,?)",
        (subject, score, total)
    )

    conn.commit()

def get_scores():

    cursor.execute("SELECT * FROM scores")

    return cursor.fetchall()

def save_flashcard(question, answer):

    cursor.execute(
        "INSERT INTO flashcards(question, answer) VALUES(?,?)",
        (question, answer)
    )

    conn.commit()

def get_flashcards():

    cursor.execute("SELECT * FROM flashcards")

    return cursor.fetchall()
