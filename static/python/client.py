# noinspection PyUnresolvedReferences
import pyodide
# noinspection PyUnresolvedReferences
from js import DOMParser, document, setInterval

# noinspection PyPackages
import weather_api

# noinspection PyPackages
from weather_api import Report


def main():
    set_weather()
    add_refresh_event()


def set_weather():
    body = document.getElementById('the_body')
    div_forecast = document.getElementById('forecast')
    div_image = document.getElementById('image')
    div_temp = document.getElementById('temp')
    div_weather = document.getElementById('weather')

    add_class(div_weather, 'hidden')
    clear_body_colors(body)

    forecast: Report = weather_api.download_report()

    add_class(body, forecast.sky)
    div_forecast.innerText = forecast.report_summary
    div_temp.innerText = str(forecast.temp) + " F"
    div_image.setAttribute('src', '/static/images/weather/{}.png'.format(forecast.sky))

    remove_class(div_weather, 'hidden')


def clear_body_colors(body):
    remove_class(body, 'cloudy')
    remove_class(body, 'sunny')
    remove_class(body, 'rain')


def add_refresh_event():
    def evt(e=None):
        set_weather()
        if e:
            e.preventDefault()
        return False

    refresh_link = document.getElementById('refresh')
    refresh_link.onclick = evt


def remove_class(element, class_name):
    element.classList.remove(class_name)


def add_class(element, class_name):
    element.classList.add(class_name)


try:
    main()
except Exception as x:
    print("Error starting weather script: {}".format(x))
