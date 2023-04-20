import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from time import sleep

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

@simplebot.command()
def rae(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Buscar definiciones en la RAE."""
    palabra = message.text.replace("/rae ", "")
    search_url = f"https://dle.rae.es/{quote_plus(palabra)}?m=form"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        sleep(1) # Agrega un retraso de 1 segundo para evitar ser bloqueado por la página web
        definiciones = soup.find_all(class_='j')
        if definiciones:
            definiciones_text = [definicion.text.strip() for definicion in definiciones]
            definiciones_text = '\n'.join(definiciones_text)
            replies.add(text=f"Definiciones de '{palabra}':\n{definiciones_text}", quote=message)
        else:
            replies.add(text=f"No se encontraron definiciones para '{palabra}'.", quote=message)
    else:
        replies.add(text=f"Error al buscar definiciones en la RAE para la palabra: {palabra}", quote=message)
