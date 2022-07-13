from pathlib import Path
import json
import requests
from datetime import datetime, timedelta
from os import listdir

# Lon lat for Molndal
request_url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/12.013/lat/57.656/data.json'
cache_file_path = './static/cache/smhi_data.json'

def get_report_phrase(sky: str):
    report_phrase = {
        'sunny': 'Clear skies and a beautiful day.',
        'cloudy': 'Cloudy skies with a chance of rain.',
        'rain': 'It will be a rainy day, bring an unbrella.',
    }
    return report_phrase[sky]

def get_weather_from_data(rain: float):
    sky = 'sunny' if rain < 1 else 'cloudy'
    sky = 'rain' if rain >= 3 else sky
    return sky

def parse_smhi_data_from_json(json_data: dict, day: int):
    approved_time = json_data['approvedTime']
    todays_date = datetime.fromisoformat(approved_time[:-1])
    parsed_data = {
        'date': '',
        'temp': [],
        'rain': []
    }
    for t in json_data['timeSeries']:
        forecast_date = datetime.fromisoformat(t['validTime'][:-1]).date()
        if forecast_date == (todays_date + timedelta(days=day)).date():
            for param in t['parameters']:
                if param['name'] == 't':
                    temp = param['values'][0]
                    parsed_data['temp'].append(temp)
                if param['name'] == 'pmean':
                    # pmean, Mean precipitation intensity, mm/h
                    rain = param['values'][0]
                    parsed_data['rain'].append(rain)
    try:
        parsed_data = {
            'date': (todays_date + timedelta(days=day)),
            'temp': sum(parsed_data['temp'])/len(parsed_data['temp']),
            'rain': sum(parsed_data['rain'])
        }
    except Exception as e:
        print('parse_smhi_data_from_json')
        print(e)
    return parsed_data

def write_cache():
    with open(cache_file_path, 'w') as f:
        data = requests.get(request_url)
        json.dump(data.json(), f) 

def read_cache():
    with open(cache_file_path, 'r') as f:
        data = json.load(f)
    return data

def update_cache():
    try: 
        with open(cache_file_path, 'r') as f:
            data = json.load(f)
            approved_date = datetime.fromisoformat(data['approvedTime'][:-1]).date()
            current_date = datetime.now().date()
        if current_date != approved_date:
            write_cache()
    except Exception as e:
        print(f'update_cache error: {e}')
        write_cache()

def get_smhi_forecast_data(day: int = 0):
    # TODO: Add timer so that i take the correct daylie forecast.
    # (Maybe download the forecast every night at 00:00?) 
    # TODO: Add geotag for dynamical lon lat updates
    # TODO: Figure out a better way of updating the cache
    update_cache()
    smhi_data = read_cache()
    parsed_data = parse_smhi_data_from_json(smhi_data, day=day)
    sky = get_weather_from_data(parsed_data['rain']) 
    data = {
        'date': parsed_data['date'],
        'sky': sky,
        'temp': parsed_data['temp'],
        'rain': round(parsed_data['rain'], 2),
        'report': get_report_phrase(sky),
    }
    # data = {
    #     'date': datetime.now().date(),
    #     'sky': 'rain',
    #     'temp': 21,
    #     'rain': 3,
    #     'report': get_report_phrase('rain'),
    # } 
    return data
