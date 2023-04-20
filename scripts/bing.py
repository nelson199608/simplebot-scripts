import requests
import random
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from bs4 import BeautifulSoup

@simplebot.command()
def yandex(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Buscar imágenes en Yandex."""
    query = message.text
    search_url = "https://yandex.com/images/search/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    params = {'text': query}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img', class_='serp-item__thumb')
        for i in range(min(len(image_tags), 5)):
            image_url = image_tags[i]['src']
            image_data = requests.get(image_url).content
            replies.add(image=image_data, quote=message)
    else:
        replies.add(text="Error al buscar imágenes en Yandex para la búsqueda: " + query)
