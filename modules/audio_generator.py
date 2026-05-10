from gtts import gTTS
import os

def generate_audio(text):

    tts = gTTS(text=text, lang='en')

    path = os.path.join(
        "summary.mp3"
    )

    tts.save(path)

    return path
