import requests
from bs4 import BeautifulSoup

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

@simplebot.command()
def subs(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Buscar subtítulos para una serie o película."""
    busqueda = message.text.replace("/subs ", "")
    busqueda_url = f"https://subswiki.com/buscar?q={busqueda}"
    response = requests.get(busqueda_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados = soup.find_all(class_='titulo')
        if resultados:
            primer_resultado = resultados[0]
            enlace = primer_resultado.find('a').get('href')
            response = requests.get(enlace)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                subs = soup.find_all("div", class_="subtitulo")
                if subs:
                    subs_text = [sub.text.strip() for sub in subs]
                    subs_text = '\n'.join(subs_text)
                    replies.add(text=f"Subtítulos para '{busqueda}':\n{subs_text}", quote=message)
                else:
                    replies.add(text=f"No se encontraron subtítulos para '{busqueda}'.", quote=message)
            else:
                replies.add(text=f"Error al buscar subtítulos para '{busqueda}'.", quote=message)
        else:
            replies.add(text=f"No se encontraron resultados para '{busqueda}'.", quote=message)
    else:
        replies.add(text=f"Error al buscar subtítulos para '{busqueda}'.", quote=message)
