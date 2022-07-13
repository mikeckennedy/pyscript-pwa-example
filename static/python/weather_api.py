from datetime import datetime
import io
import json

# noinspection PyUnresolvedReferences
import pyodide


class Report:
    # noinspection PyDefaultArgument
    def __init__(self, data={}):
        self.report_summary: str = data.get('report')
        self.temp: int = int(data.get('temp', 0))
        self.rain: float = float(data.get('rain', 0))
        self.sky: str = data.get('sky')
        self.date: datetime = data.get('date')



def download_report(weekday_nr: int) -> Report:
    if weekday_nr == 0:
        resp: io.StringIO = pyodide.open_url('/weather/data')
        forecast = json.loads(resp.read())
    else:
        resp: io.StringIO = pyodide.open_url(f'/weather/data/{weekday_nr}')
        forecast = json.loads(resp.read()) 
    return Report(forecast)
