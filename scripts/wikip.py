import simplebot
from deltabot import DeltaBot
from wikipedia import wikipedia
from simplebot_instantview import generate_iv

@simplebot.command
def wiki(bot: DeltaBot, payload: str, message: simplebot.Message) -> None:
    try:
        page = wikipedia.page(payload)
        summary = wikipedia.summary(payload)
        iv_url = generate_iv(f"{page.title}\n\n{summary}")
        bot.send_text(message.chat, f"{page.title}\n\n{summary}\n\n{iv_url}")
    except wikipedia.exceptions.PageError:
        bot.send_text(message.chat, f"No se encontró una página de Wikipedia para: {payload}")
    except wikipedia.exceptions.DisambiguationError as e:
        bot.send_text(message.chat, f"{e}\n\nPor favor especifica más tu búsqueda.")

simplebot.run()
