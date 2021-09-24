import base64
import os
import utils

from flask import Flask, render_template, request
from config import Config


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: /'


@app.route('/generate')
def generate():
    name = request.args.get('name')
    username = request.args.get('username')
    text = request.args.get('text')
    pic = request.args.get('pic')

    if None in (name, username, text):
        return render_template('error.html', error_desc="Ci sono dei parametri mancanti, torna indietro."), 400

    if pic is not None:
        pic = utils.get_instagram_pic_stream(pic)

    if pic is None:
        pic = './images/1080x1080.png'

    img = utils.get_sticker_photo_stream(text, name, username, pic)
    encoded_img = base64.b64encode(img.getvalue())
    decoded_img = encoded_img.decode('utf-8')
    img_data = f"data:image/jpeg;base64,{decoded_img}"
    return render_template('generate.html', img_data=img_data)


if __name__ == '__main__':
    if Config.debug:
        os.environ['FLASK_ENV'] = 'development'
    app.run(Config.host, Config.port, Config.debug)
