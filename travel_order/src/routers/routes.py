from fastapi import APIRouter, HTTPException

from src.models.trip import TripResponse
from src.services.trip_service import find_shortest_trip
from src.services.spacy_service import get_origin_and_destination

router = APIRouter()


@router.get("/shortest-trip", response_model=TripResponse)
def get_shortest_trip(departure_city: str, arrival_city: str):
    result = find_shortest_trip(departure_city, arrival_city)

    if not result:
        raise HTTPException(status_code=404, detail="No path found between the cities")

    return result


@router.get("/sentence/shortest-trip", response_model=TripResponse)
def get_shortest_trip_with_sentence(sentence: str):
    result = get_origin_and_destination(sentence)

    if not result:
        raise HTTPException(status_code=404, detail="No path found between the cities")

    return result
