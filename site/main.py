import base64

from flask import Flask, render_template, request

import config
import utils

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: /'


@app.route('/generate')
def generate():
    name: str = request.args.get('name')
    username: str = request.args.get('username')
    text: str = request.args.get('text')
    pic: str = request.args.get('pic')

    if None in (name, username, text):
        return render_template('error.html', error_desc="There are missing parameters, go back."), 400

    if pic is not None:
        if pic.startswith('https://') or pic.startswith('https://'):
            pic = utils.get_url_pic_stream(pic)
        else:
            pic = utils.get_instagram_pic_stream(pic)

    if pic is None:
        pic = './images/1080x1080.png'

    img = utils.get_sticker_photo_stream(text, name, username, pic)
    encoded_img = base64.b64encode(img.getvalue())
    decoded_img = encoded_img.decode('utf-8')
    img_data = f"data:image/jpeg;base64,{decoded_img}"
    return render_template('generate.html', img_data=img_data)


if __name__ == '__main__':
    app.run(config.HOST, config.PORT, False)
