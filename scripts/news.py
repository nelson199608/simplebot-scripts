import simplebot
from deltabot import DeltaBot
import requests
from bs4 import BeautifulSoup

@simplebot.command
def news(bot: DeltaBot, payload: str, message: simplebot.Message) -> None:
    url = f'https://news.google.com/search?q={payload}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne')
    for article in articles[:4]:
        title = article.find('h3', class_='ipQwMb ekueJc RD0gLb').text
        link = article.find('a', class_='VDXfz')['href']
        message.chat.send_text(title + '\n' + link)

if __name__ == '__main__':
    simplebot.run()
