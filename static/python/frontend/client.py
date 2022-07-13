# noinspection PyUnresolvedReferences
from datetime import datetime
# noinspection PyUnresolvedReferences,PyPackageRequirements
import pyodide
# noinspection PyUnresolvedReferences,PyPackageRequirements
from js import DOMParser, document, setInterval, console

# noinspection PyPackages
import weather_frontend_api 
from weather_report import WeatherReport


def main():
    print('before clock')
    view_clock()
    print('before weather')
    set_all_weather()
    print('before refresh event')
    add_refresh_event()


def set_all_weather():
    set_main_weather()
    for forecast_day in range(1,7):
        set_span_weather(forecast_day) 


def view_clock():
    body = document.getElementById('the_body')
    div_clock = document.getElementById('clock')
    add_class(div_clock, 'hidden')
    clear_body_colors(body)
    div_clock.innerText = str(datetime.now().strftime("%H:%M"))
    remove_class(div_clock, 'hidden')


def get_forecast(forecast_day: int = 0):
    try:
        forecast: WeatherReport = weather_frontend_api.download_report(forecast_day)
    except Exception as x:
        console.log("Error calling weather API: {}".format(x))
        forecast = create_error_style_report()
    return forecast

def set_span_weather(forecast_day: int):
    body = document.getElementById('the_body')
    div_forecast = document.getElementById(f'forecast-small-{forecast_day}')
    div_image = document.getElementById(f'image-small-{forecast_day}')
    div_temp = document.getElementById(f'temp-small-{forecast_day}')
    div_weather = document.getElementById(f'weather-small-{forecast_day}')
    div_date = document.getElementById(f'date-small-{forecast_day}')
    div_rain = document.getElementById(f'rain-small-{forecast_day}')

    add_class(div_weather, 'hidden')
    clear_body_colors(body)

    forecast = get_forecast(forecast_day)
    add_class(body, forecast.sky)
    div_date.innerText = forecast.date[:-17]
    div_image.setAttribute('src', '/static/images/weather/{}.png'.format(forecast.sky))
    div_temp.innerText = str(forecast.temperature_in_c) + " °C"
    div_rain.innerText = str(forecast.rain_in_mm) + " mm"
    div_forecast.innerText = forecast.report_summary

    remove_class(div_weather, 'hidden')
 
def set_main_weather():
    body = document.getElementById('the_body')
    div_forecast = document.getElementById('forecast')
    div_image = document.getElementById('image')
    div_temp = document.getElementById('temp')
    div_weather = document.getElementById('weather')
    div_date = document.getElementById('date')
    div_rain = document.getElementById('rain')

    add_class(div_weather, 'hidden')
    clear_body_colors(body)

    forecast = get_forecast()
    add_class(body, forecast.sky)
    # TODO: Figure out werid crash when i try to convert to date here
    div_date.innerText = forecast.date[:-12]
    div_image.setAttribute('src', '/static/images/weather/{}.png'.format(forecast.sky))
    div_temp.innerText = str(forecast.temperature_in_c) + " °C"
    div_rain.innerText = str(forecast.rain_in_mm) + " mm"
    div_forecast.innerText = forecast.report_summary

    remove_class(div_weather, 'hidden')


def create_error_style_report():
    forecast = WeatherReport()
    forecast.sky = 'offline'
    forecast.report_summary = 'Weather API is offline.'
    return forecast


def clear_body_colors(body):
    classes = ['cloudy', 'sunny', 'rain', 'offline']
    for c in classes:
        remove_class(body, c)


def add_refresh_event():
    def evt(e=None):
        view_clock()
        set_all_weather()
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
