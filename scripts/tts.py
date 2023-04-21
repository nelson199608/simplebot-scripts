import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

@simplebot.command()
def text_to_speech(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Convertir texto a voz."""
    texto = message.text.replace("/speech ", "")
    tts = gTTS(texto, lang='es')
    tts.save("speech.mp3")
    os.system("mpg321 speech.mp3") # Reproducir el archivo de audio utilizando mpg321
    replies.add(text=f"Convertido texto a voz: '{texto}'", quote=message)
