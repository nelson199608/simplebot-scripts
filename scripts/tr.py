import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from translate import Translator

@simplebot.command
def translate(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Translate any text in private."""
    if not replies.has_replies() and not message.chat.is_multiuser() and message.text:
        translated_text = _translate(message.text)
        replies.add(text=translated_text, quote=message)

def _translate(text: str, target_language: str = 'en') -> str:
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text
