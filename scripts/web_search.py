from urllib.parse import quote_plus
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session # noqa

@simplebot.filter(trylast=True)
def search_filter(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Send me any text in private to search in the web."""
    if not replies.has_replies() and not message.chat.is_multiuser() and message.text:
        text, html = _search(bot.self_contact.addr, message.text)
        replies.add(text=text or "Search results", html=html, quote=message)

def _search(bot_addr: str, query: str) -> tuple:
    # Usamos la versión html de duckduckgo en lugar de la lite, porque tiene más información y opciones
    with session.get(f"https://duckduckgo.com/html?q={quote_plus(query)}") as resp:
        resp.raise_for_status()
        # Usamos el parámetro t=ffab para indicar que estamos usando un navegador Firefox
        return prepare_html(bot_addr, resp.url + "&t=ffab", resp.text)
