from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherReport:
    sky: str = ''
    date: datetime = None
    rain_in_mm: float = 0.0
    temperature_in_c: int = 0.0
    report_summary: str = ''