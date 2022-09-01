import datetime as dtm
import logging
from io import BytesIO
from textwrap import fill
from typing import Union, cast

import pytz
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features

import config
from const import (
    HEADER_TEMPLATE,
    FOOTER_TEMPLATE,
    BODY_TEMPLATE,
    VERIFIED_IMAGE,
    TEXT_MAIN,
    TEXT_SECONDARY,
    FOOTER_FONT,
    USER_NAME_FONT,
    USER_HANDLE_FONT,
    SMALL_TEXT_FONT,
)

logs = logging.getLogger(__name__)

TEXT_DIRECTION_SUPPORT = features.check('raqm')


def mask_circle_transparent(image: Union[Image.Image, str]) -> Image.Image:
    """
    Cuts a circle from a square image.

    Args:
        image: Either the image path or a loaded :class:`PIL.Image.Image`.

    Returns:
        :class:`PIL.Image.Image`:
    """
    if isinstance(image, str):
        image = Image.open(image)

    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)
    mask = mask.filter(ImageFilter.DETAIL())

    result = image.copy()
    result.putalpha(mask)

    return result


def shorten_text(text: str, max_width: int, font: ImageFont.ImageFont) -> str:
    """
    Shortens the given text such that it does not exceed ``max_width`` pixels wrt the given
    ``font``. Trailing dots are added to indicate that the text was shortened.

    Args:
        text: The text to shorten.
        max_width: Maximum width in pixels.
        font: The font the shortening is executed for.

    Returns:
        str: The shortened text.
    """
    width, _ = font.getsize(text)
    i = 0
    short_text = text
    while width > max_width:
        i += 1
        short_text = f"{text[:-i]}..."
        width, _ = font.getsize(short_text)
    return short_text


def build_footer(timezone: str = "UTC") -> Image.Image:
    """
    Creates the footer for the sticker by adding the current timestamp.

    Args:
        timezone: Optional. The timezone to use for the timestamp. Must be one of the timezones
          supported by ``pytz``. Defaults to ``'Europe/Berlin'``.

    Returns:
        :class:`PIL.Image.Image`: The footer as Pillow image.
    """
    now = dtm.datetime.now(tz=pytz.timezone(timezone))
    date_string = " ".join([now.strftime("%I:%M %p"), "•", now.strftime("%b %d, %Y")])

    # Offsets
    top = 28*2
    left = 27*2

    image = Image.open(FOOTER_TEMPLATE)
    draw = ImageDraw.Draw(image)
    draw.text((left, top), date_string, fill=TEXT_SECONDARY, font=FOOTER_FONT)
    return image


def build_header(name: str, username: str, user_picture: Image.Image, verified: bool = False) -> Image.Image:
    """
    Creates the header for the sticker customized for the given user. The header will be saved as
    file and can be reused.

    Args:
        name: The name for the user header.
        username: The username for the user this header is build for.
        user_picture: Optional. The profile picture of the user. Defaults to the bots' logo.
        verified: Add verified logo

    Returns:
        :class:`PIL.Image.Image`: The header as Pillow image.
    """

    # Get Background
    background: Image = Image.open(HEADER_TEMPLATE)

    # Add user picture
    up_left = 25*2
    up_top = 25*2

    # crop a centered square
    if not user_picture.width == user_picture.height:
        side = min(user_picture.width, user_picture.height)
        left = (user_picture.width - side) // 2
        upper = (user_picture.height - side) // 2
        user_picture = user_picture.crop((left, upper, left + side, upper + side))

    # make it a circle a small
    user_picture = mask_circle_transparent(user_picture)
    user_picture.thumbnail((78*2, 78*2))
    background.alpha_composite(user_picture, (up_left, up_top))
    draw = ImageDraw.Draw(background)

    # Add username
    un_left = 118*2
    un_top = 30*2
    user_name = shorten_text(cast(str, name), 314*2, USER_NAME_FONT)
    draw.text((un_left, un_top), user_name, fill=TEXT_MAIN, font=USER_NAME_FONT)

    # Add user handle
    uh_left = 118*2
    uh_top = 62*2
    user_handle = shorten_text(
        f"@{username}", 370*2, USER_HANDLE_FONT
    )
    draw.text((uh_left, uh_top), user_handle, fill=TEXT_SECONDARY, font=USER_HANDLE_FONT)

    # Add verified symbol
    if verified:
        (un_width, _), _ = USER_NAME_FONT.font.getsize(user_name)
        v_left = un_left + un_width + 4*2
        v_top = 34*2
        background.alpha_composite(VERIFIED_IMAGE, (v_left, v_top))

    return background


def build_body(text: str) -> Image.Image:
    """
    Builds the body for the sticker by setting the given text.

    Args:
        text: The text to display.

    Returns:
        :class:`PIL.Image.Image`: The body as Pillow image.
    """
    max_chars_per_line = 35
    left = 27*2

    def multiline_text(position, text_, background_):
        spacing = 4
        _, height = SMALL_TEXT_FONT.getsize_multiline(text_, spacing=spacing)
        background_ = background_.resize((background_.width, height - spacing+5))
        draw = ImageDraw.Draw(background_)
        draw.multiline_text(position, text_, font=SMALL_TEXT_FONT, spacing=spacing, anchor='la', align='left', fill=TEXT_MAIN)

        return background_

    background = Image.open(BODY_TEMPLATE)
    top = -15

    lines = text.split("\n")
    text = "\n".join([fill(line, max_chars_per_line, break_on_hyphens=True) for line in lines])
    text = "\n".join(text.split('\n')[:9])
    background = multiline_text((left, top), text, background)
    return background


def build_sticker(text: str, name: str, username: str, pic: Union[str, Image.Image]) -> Image.Image:
    """
    Builds the sticker header, body and footer.

    Arguments:
        text: Text of the tweet.
        name: Name to display on the tweet.
        username: Username to display on the tweet.
        pic: Path of the tweet image.

    Returns:
        :class:`PIL.Image.Image`: The sticker as Pillow image.
    """

    header = build_header(name, username, Image.open(pic))
    body = build_body(text)
    footer = build_footer(timezone='Europe/Berlin')
    sticker = Image.new("RGBA", (1024, 1024))
    sticker.paste(header, (0, 0))
    sticker.paste(footer, (0, 1024 - footer.height))

    h = header.height

    while h < (1024-footer.height):
        b = Image.open(BODY_TEMPLATE)
        sticker.paste(b, (0, h))
        h += b.height

    sticker.paste(body, (0, header.height))
    sticker.thumbnail((1024, 1024))

    return sticker


def get_sticker_photo_stream(text: str, name: str, username: str, pic: Union[str, Image.Image]) -> BytesIO:
    """
    Get the sticker image stream.

    Args:
        text: The text to display on the tweet.
        name: name to display on the tweet.
        username: username to display on the tweet.
        pic: Path of the tweet image or Pillow Image.

    Returns:
        BytesIO: Bytes of the sticker
    """
    sticker_stream = BytesIO()
    sticker = build_sticker(text, name, username, pic)
    sticker.save(sticker_stream, format="PNG")
    sticker_stream.seek(0)

    return sticker_stream


def get_instagram_pic_stream(username: str) -> BytesIO:
    """
    Get instagram profile picture by username

    Args:
        username: Instagram username

    Returns:
        BytesIO: The photo as BytesIO.
    """
    req_url = f'https://www.instagram.com/{username}/?__a=1'
    head = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    }
    r = requests.get(req_url, headers=head, cookies={'sessionid': config.SESSION_ID})
    try:
        req_json = r.json()
    except (Exception, ) as err:
        print(err)
        return None
    if req_json == {}:
        return None
    pic_url = req_json.get('graphql', {}).get('user', {}).get('profile_pic_url_hd')
    if pic_url is None:
        return None

    return BytesIO(requests.get(pic_url, stream=True, headers=head).content)


def get_url_pic_stream(url: str) -> BytesIO:
    """
    Get picture stream by link

    Args:
        url: Link of the image

    Returns:
        BytesIO: The photo as BytesIO.
    """
    try:
        return BytesIO(requests.get(url, stream=True).content)
    except (Exception, ):
        return None
