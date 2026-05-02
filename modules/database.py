%%writefile database.py
import sqlite3

conn = sqlite3.connect("study.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS scores(
subject TEXT,
score INT,
total INT
)
""")
conn.commit()

def save(subject, score, total):
    c.execute("INSERT INTO scores VALUES(?,?,?)",(subject,score,total))
    conn.commit()

def get():
    c.execute("SELECT subject,score,total FROM scores")
    return c.fetchall()

