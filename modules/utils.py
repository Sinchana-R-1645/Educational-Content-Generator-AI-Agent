import re
import streamlit as st
from groq import Groq

def get_client():

    key = st.secrets["GROQ_API_KEY"]

    return Groq(api_key=key)

def llm(prompt):

    client = get_client()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

def clean_json(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if match:
        return match.group(0)

    return text
