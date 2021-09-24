from pathlib import Path
from PIL import Image, ImageFont

PATH_PREFIX = '../' if Path('../headers').is_dir() else ''

TEMPLATE_DIRECTORY = f"{PATH_PREFIX}images"
""":obj:`str`: Name of the directory containing the imagesimages."""

HEADER_TEMPLATE = f"{TEMPLATE_DIRECTORY}/header.png"
""":obj:`str`: Path of the template for the header."""

FOOTER_TEMPLATE = f"{TEMPLATE_DIRECTORY}/footer.png"
""":obj:`str`: Path of the template for the footer."""

BODY_TEMPLATE = f"{TEMPLATE_DIRECTORY}/body.png"
""":obj:`str`: Path of the template for the body."""

VERIFIED_TEMPLATE = f"{TEMPLATE_DIRECTORY}/verified.png"
""":obj:`str`: Path of the template for the »verified« symbol."""

VERIFIED_IMAGE = Image.open(VERIFIED_TEMPLATE)
""":class:`Pillow.Image.Image`: The »verified« symbol as Pillow image in the correct size."""

VERIFIED_IMAGE.thumbnail((27*2, 27*2))

TEXT_MAIN = "#ffffff"
""":obj:`str`: Color of the main text."""

TEXT_SECONDARY = "#8d99a5ff"
""":obj:`str`: Color of secondary text."""

FONTS_DIRECTORY = f"{PATH_PREFIX}fonts"
""":obj:`str`: Name of the directory containing the fonts."""

FONT_HEAVY = f"{FONTS_DIRECTORY}/seguibl.ttf"
""":obj:`str`: Font of the main text."""

FONT_SEMI_BOLD = f"{FONTS_DIRECTORY}/seguisb.ttf"
""":obj:`str`: Font of the secondary text."""

FOOTER_FONT = ImageFont.truetype(FONT_SEMI_BOLD, 35)
""":class:`PIL.ImageFont.Font`: Font to use for the footer."""

USER_NAME_FONT = ImageFont.truetype(FONT_HEAVY, 24*2)
""":class:`PIL.ImageFont.Font`: Font to use for the username."""

USER_HANDLE_FONT = ImageFont.truetype(FONT_SEMI_BOLD, 23*2)
""":class:`PIL.ImageFont.Font`: Font to use for the user handle."""

SMALL_TEXT_FONT = ImageFont.truetype(FONT_SEMI_BOLD, 55)
""":class:`PIL.ImageFont.Font`: Font to use for small text in the body."""
