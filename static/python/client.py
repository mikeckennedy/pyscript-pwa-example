# noinspection PyUnresolvedReferences
import random

# noinspection PyUnresolvedReferences,PyPackageRequirements
import pyodide
# noinspection PyUnresolvedReferences,PyPackageRequirements
from js import DOMParser, document, setInterval, console

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

    try:
        forecast: Report = weather_api.download_report()
    except Exception as x:
        console.log("Error calling weather API: {}".format(x))
        forecast = create_error_style_report()

    add_class(body, forecast.sky)
    div_forecast.innerText = forecast.report_summary
    div_temp.innerText = str(forecast.temp) + " F"
    div_image.setAttribute('src', '/static/images/weather/{}.png'.format(forecast.sky))

    remove_class(div_weather, 'hidden')


def create_error_style_report():
    forecast = Report()
    forecast.sky = 'offline'
    forecast.temp = 0
    forecast.report_summary = 'Weather API is offline.'
    return forecast


def clear_body_colors(body):
    classes = ['cloudy', 'sunny', 'rain', 'offline']
    for c in classes:
        remove_class(body, c)


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
