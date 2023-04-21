import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

@simplebot.command()
def tts(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Convertir texto a voz."""
    texto = message.text.replace("/tts ", "")
    if not texto:
        replies.add(text="Debes proporcionar un texto para convertir a voz.", quote=message)
        return
    audio_path = "speech.mp3"
    tts = gTTS(texto, lang='es')
    tts.save(audio_path)
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
        bot.send_audio(message.chat_id, audio_data, caption=f"Audio de texto a voz: '{texto}'")
    os.remove(audio_path)
