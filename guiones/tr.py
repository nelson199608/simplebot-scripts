import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from translate import Translator

@simplebot.command
def translate(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Translate text in private. Usage: /translate <target_language> <text_to_translate>"""
    if not replies.has_replies() and not message.chat.is_multiuser() and message.text:
        # Dividir el mensaje en el idioma de destino y el texto a traducir
        language, text = _parse_message(message.text)
        # Realizar la traducción
        translated_text = _translate(text, target_language=language)
        # Agregar la respuesta al bot
        replies.add(text=translated_text, quote=message)

def _parse_message(message_text: str) -> tuple[str, str]:
    """Parse the message to extract the target language and the text to translate."""
    # Eliminar el comando "/translate" del mensaje
    text = message_text.replace("/translate", "").strip()
    # Dividir el mensaje en el idioma de destino y el texto a traducir
    language, text = text.split(maxsplit=1)
    # Eliminar la sigla del idioma del texto a traducir
    text = text.replace(language, "").strip()
    return language, text

def _translate(text: str, target_language: str = 'en') -> str:
    """Translate the text to the target language."""
    translator = Translator(to_lang=target_language)
    translated_text = translator.translate(text)
    return translated_text
