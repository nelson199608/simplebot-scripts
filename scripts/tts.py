import functools
import io
import mimetypes
import re
from typing import Generator
from urllib.parse import quote

import bs4
import requests
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
)
session.request = functools.partial(session.request, timeout=15)  # type: ignore


@simplebot.command
def image(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Get an image based on the given text.

    Example:
    /image cats and dogs
    """
    _image_cmd(1, bot, payload, message, replies)


@simplebot.command
def image5(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Search for images, returns up to five results.

    Example:
    /image5 roses
    """
    _image_cmd(5, bot, payload, message, replies)


def _image_cmd(
    img_count: int, bot: DeltaBot, payload: str, message: Message, replies: Replies
) -> None:
    if not payload:
        replies.add(text="❌ No text given", quote=message)
        return
    imgs = img_count
    for filename, data in _get_images(bot, payload):
        replies.add(filename=filename, bytefile=io.BytesIO(data))
        imgs -= 1
        if imgs <= 0:
            break
    if imgs == img_count:
        replies.add(text="❌ No results", quote=message)


def _get_images(bot: DeltaBot, query: str) -> Generator:
    img_providers = [_bing_imgs]
    while img_providers:
        provider = img_providers.pop()
        try:
            bot.logger.debug("Trying %s", provider)
            for img_url in provider(query):
                with session.get(img_url) as resp:
                    resp.raise_for_status()
                    filename = "image" + (get_extension(resp) or ".jpg")
                    yield filename, resp.content
        except Exception as err:
            bot.logger.exception(err)


def _bing_imgs(query: str) -> set:
    url = f"https://www.bing.com/images/search?q={quote(query)}&form=HDRSC2"
    with session.get(url) as resp:
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
    links = set()
    for tag in soup("img", class_="mimg"):
        if tag["src"].startswith("data:"):
            continue
        links.add(tag["src"])
    return links


def get_extension(resp: requests.Response) -> str:
    disp = resp.headers.get("content-disposition")
    if disp is not None and re.findall("filename=(.+)", disp):
        fname = re.findall("filename=(.+)", disp)[0].strip('"')
    else:
        fname = resp.url.split("/")[-1].split("?")[0].split("#")[0]
    if "." in fname:
        ext = "." + fname.rsplit(".", maxsplit=1)[-1]
    else:
        ctype = resp.headers.get("content-type", "").split(";")[0].strip().lower()
        ext = mimetypes.guess_extension(ctype) or ""
    return ext
