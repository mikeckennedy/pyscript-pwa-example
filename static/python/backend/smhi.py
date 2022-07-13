# Standard libraries
import json
import requests
from datetime import datetime, timedelta
# Local imports
from static.python.backend.provider import ForecastData

# Lon lat for Molndal

class SHMIProvider:
    def __init__(self, provider_name: str, request_url: str, cache_file_path: str):
        self.provider_name = provider_name
        self.request_url = request_url
        self.cache_file_path = cache_file_path

    # Local caching
    def write_cache(self):
        with open(self.cache_file_path, 'w') as f:
            data = requests.get(self.request_url)
            json.dump(data.json(), f) 

    def read_cache(self):
        with open(self.cache_file_path, 'r') as f:
            data = json.load(f)
        return data

    def update_cache(self):
        try: 
            with open(self.cache_file_path, 'r') as f:
                data = json.load(f)
                approved_date = datetime.fromisoformat(data['approvedTime'][:-1]).date()
                current_date = datetime.now().date()
            if current_date != approved_date:
                self.write_cache()
        except FileNotFoundError as e:
            print(f'update_cache error: {e}')
            self.write_cache()

    # Parsing data from SMHI
    def parse_data_from_request(self, json_data: dict, day: int):
        approved_time = json_data['approvedTime']
        todays_date = datetime.fromisoformat(approved_time[:-1])
        tempratures = []
        accumulated_rain = []
        for t in json_data['timeSeries']:
            forecast_date = datetime.fromisoformat(t['validTime'][:-1]).date()
            if forecast_date == (todays_date + timedelta(days=day)).date():
                for param in t['parameters']:
                    # SMHI specific parameter names, link to docs
                    # https://opendata.smhi.se/apidocs/metfcst/parameters.html
                    if param['name'] == 't':
                        temp = param['values'][0]
                        tempratures.append(temp)
                    if param['name'] == 'pmean':
                        # pmean, Mean precipitation intensity, mm/h
                        rain = param['values'][0]
                        accumulated_rain.append(rain)
        try:
            parsed_data = {
                'date': (todays_date + timedelta(days=day)),
                'temperature_in_c': sum(tempratures)/len(tempratures),
                'rain_in_mm': sum(accumulated_rain)
            }
        except Exception as e:
            print('parse_smhi_data_from_json')
            print(e)
        return parsed_data

    # Returing ForecastData dataclass accordning to WeatherProviderProtocal
    def get_forecast_data(self, day: int) -> ForecastData:
        self.update_cache()
        smhi_data = self.read_cache()
        parsed_data = self.parse_data_from_request(smhi_data, day=day)
        return ForecastData(**parsed_data)
