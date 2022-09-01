from pathlib import Path
from PIL import Image, ImageFont

PATH_PREFIX = '../' if Path('../headers').is_dir() else ''

TEMPLATE_DIRECTORY = f"{PATH_PREFIX}images"

HEADER_TEMPLATE = f"{TEMPLATE_DIRECTORY}/header.png"

FOOTER_TEMPLATE = f"{TEMPLATE_DIRECTORY}/footer.png"

BODY_TEMPLATE = f"{TEMPLATE_DIRECTORY}/body.png"

VERIFIED_TEMPLATE = f"{TEMPLATE_DIRECTORY}/verified.png"

VERIFIED_IMAGE = Image.open(VERIFIED_TEMPLATE)

VERIFIED_IMAGE.thumbnail((27*2, 27*2))

TEXT_MAIN = "#ffffff"

TEXT_SECONDARY = "#8d99a5ff"

FONTS_DIRECTORY = f"{PATH_PREFIX}fonts"

FONT_HEAVY = f"{FONTS_DIRECTORY}/seguibl.ttf"

FONT_SEMI_BOLD = f"{FONTS_DIRECTORY}/seguisb.ttf"

FOOTER_FONT = ImageFont.truetype(FONT_SEMI_BOLD, 35)

USER_NAME_FONT = ImageFont.truetype(FONT_HEAVY, 24*2)

USER_HANDLE_FONT = ImageFont.truetype(FONT_SEMI_BOLD, 23*2)

SMALL_TEXT_FONT = ImageFont.truetype(FONT_SEMI_BOLD, 55)
