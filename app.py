import json
import random
from pathlib import Path

import flask

app = flask.Flask(__name__)


@app.get('/')
def index():
    return flask.render_template('index.html')


# @app.get('/weather')
# def weather():
#     return flask.render_template('weather.html')


@app.get('/weather/data')
def weather_data():
    data = get_random_report()
    return flask.jsonify(data)


@app.get('/serviceWorker.js')
def worker():
    js = Path(__file__).parent / 'static' / 'js' / 'serviceWorker.js'
    text = js.read_text()
    resp = flask.make_response(text)
    resp.content_type = 'application/javascript'
    resp.headers['Service-Worker-Allowed'] = '/'

    return resp


def get_random_report() -> dict:
    reports = [
        {
            'report': 'Clear and beautify skies today.',
            'sky': 'sunny',
            'temp': random.randint(65, 88),
        },
        {
            'report': 'Cloudy and a bit cool today.',
            'sky': 'cloudy',
            'temp': random.randint(48, 60),
        },
        {
            'report': 'Are those icicles falling from the sky? Get inside.',
            'sky': 'rain',
            'temp': random.randint(33, 40),
        }
    ]

    return random.choice(reports)
