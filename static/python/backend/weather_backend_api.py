
# Local imports
from static.python.frontend.weather_report import WeatherReport
from static.python.backend.provider import WeatherProviderProtocal, ForecastData
from static.python.backend.smhi import SHMIProvider

# Define specific weather provider detalis here
request_url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/12.013/lat/57.656/data.json'
cache_file_path = './static/cache/weather_data.json'
smhi_provider = SHMIProvider('SMHI', request_url, cache_file_path)

class WeatherBackendAPI:
    def __init__(self, provider: WeatherProviderProtocal):
       self.provider = provider

    # Weather related logic
    def get_report_phrase(self, sky: str):
        report_phrase = {
            'sunny': 'Clear skies and a beautiful day.',
            'cloudy': 'Cloudy skies with a chance of rain.',
            'rain': 'It will be a rainy day, bring an unbrella.',
        }
        return report_phrase[sky]

    def get_weather_from_data(self, rain: float):
        sky = 'sunny' if rain < 1 else 'cloudy'
        sky = 'rain' if rain >= 3 else sky
        return sky

    def get_forecast_data(self, day: int = 0) -> WeatherReport:
        # TODO: Add timer so that i take the correct daylie forecast.
        # (Maybe download the forecast every night at 00:00?) 
        # TODO: Add geotag for dynamical lon lat updates
        data: ForecastData = self.provider.get_forecast_data(day)
        sky = self.get_weather_from_data(data.rain_in_mm) 
        weather_report_data = {
            'sky': sky,
            'date': data.date,
            'rain_in_mm': round(data.rain_in_mm, 2),
            'temperature_in_c': int(data.temperature_in_c),
            'report_summary': self.get_report_phrase(sky),
        }
        return WeatherReport(**weather_report_data)
    
    @classmethod
    def setup(cls) -> "WeatherBackendAPI":
        return cls(smhi_provider)