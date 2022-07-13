# Standard library imports
from pathlib import Path
# Third party imports 
import flask
# Local imports 
from static.python.backend.weather_backend_api import WeatherBackendAPI

app = flask.Flask(__name__)
print('Before ws backend')
ws_backend = WeatherBackendAPI.setup()
print('After ws backend')
print(ws_backend.provider.provider_name)

@app.get('/')
def index():
    return flask.render_template('index.html')

@app.get('/weather/data')
def weather_data():
    data = ws_backend.get_forecast_data()
    return flask.jsonify(data)

@app.get('/weather/data/<forecast_day>')
def weather_data_weekday(forecast_day):
    data = ws_backend.get_forecast_data(int(forecast_day))
    return flask.jsonify(data)

@app.get('/serviceWorker.js')
def worker():
    app.logger.info('serviceWorker.js just started!')
    js = Path(__file__).parent / 'static' / 'js' / 'serviceWorker.js'
    text = js.read_text()
    resp = flask.make_response(text)
    resp.content_type = 'application/javascript'
    resp.headers['Service-Worker-Allowed'] = '/'

    return resp

