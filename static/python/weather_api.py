import io
import json

# noinspection PyUnresolvedReferences
import pyodide


class Report:
    # noinspection PyDefaultArgument
    def __init__(self, data={}):
        self.report_summary: str = data.get('report')
        self.sky: str = data.get('sky')
        self.temp: int = int(data.get('temp', 0))


def download_report() -> Report:
    resp: io.StringIO = pyodide.open_url('/weather/data')
    forecast = json.loads(resp.read())

    return Report(forecast)
