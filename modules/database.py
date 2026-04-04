import sqlite3
from datetime import datetime

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
        weak_areas TEXT,
        timestamp TEXT
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
    INSERT INTO performance (score, weak_areas, timestamp)
    VALUES (?, ?, ?)
    """, (score, str(weak_areas), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()


def get_stats():
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(score) FROM performance")
    total, avg = cursor.fetchone()

    conn.close()

    return total or 0, round(avg or 0, 2)


def get_last_performance():
    conn = sqlite3.connect("study.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT score, weak_areas FROM performance 
    ORDER BY id DESC LIMIT 1
    """)
    data = cursor.fetchone()

    conn.close()

    if data:
        return data[0], eval(data[1])
    return None, None
