
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class ForecastData:
    date: datetime
    temperature_in_c: float
    rain_in_mm: float


class WeatherProviderProtocal(Protocol):
    provider_name: str
    request_url: str
    cache_file_path: str

    def parse_data_from_request() -> dict:
        raise NotImplementedError

    def get_forecast_data() -> ForecastData:
        raise NotImplementedError

    def read_cache() -> None:
        raise NotImplementedError

    def write_cache() -> None:
        raise NotImplementedError
    
    def update_cache() -> None:
        raise NotImplementedError


