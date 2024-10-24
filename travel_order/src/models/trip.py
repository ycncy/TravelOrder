from pydantic import BaseModel
from typing import List


class TripStep(BaseModel):
    departure_station: str
    arrival_station: str
    travel_time: float
    departure_city: str
    arrival_city: str
    stop_lat_start: float
    stop_lon_start: float
    stop_lat_end: float
    stop_lon_end: float


class TripResponse(BaseModel):
    total_time: float
    steps: List[TripStep]


class TripOptionsResponse(BaseModel):
    departures: List[str]
    arrivals: List[str]
