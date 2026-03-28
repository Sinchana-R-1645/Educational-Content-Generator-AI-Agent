import sqlite3
import ast

def create_db():
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_text TEXT,
        quiz TEXT,
        flashcards TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score REAL,
        weak_areas TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_data(input_text, quiz, flashcards):
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO content (input_text, quiz, flashcards)
    VALUES (?, ?, ?)
    """, (input_text, str(quiz), str(flashcards)))

    conn.commit()
    conn.close()


def save_performance(score, weak_areas):
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO performance (score, weak_areas)
    VALUES (?, ?)
    """, (score, str(weak_areas)))

    conn.commit()
    conn.close()


def get_last_performance():
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("SELECT score, weak_areas FROM performance ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    conn.close()

    if data:
        return data[0], ast.literal_eval(data[1])
    return None, None
