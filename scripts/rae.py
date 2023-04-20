import requests
import random
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
from simplebot_instanview import show

@simplebot.command()
def rae(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Buscar definiciones en la RAE."""
    palabra = message.text.replace("/rae ", "")
    search_url = f"https://dle.rae.es/{palabra}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        definiciones = soup.find_all(class_='j')
        if definiciones:
            definiciones_text = [definicion.text.strip() for definicion in definiciones]
            definiciones_text = '\n'.join(definiciones_text)
            show(f"Definiciones de '{palabra}':\n{definiciones_text}")
            replies.add(text=f"Definiciones de '{palabra}':\n{definiciones_text}", quote=message)
        else:
            show(f"No se encontraron definiciones para '{palabra}'.")
            replies.add(text=f"No se encontraron definiciones para '{palabra}'.", quote=message)
    else:
        show(f"Error al buscar definiciones en la RAE para la palabra: {palabra}")
        replies.add(text=f"Error al buscar definiciones en la RAE para la palabra: {palabra}", quote=message)
