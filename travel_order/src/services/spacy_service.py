from src.models.trip import TripResponse
from src.services.trip_service import find_shortest_trip

from src.config.loader import spacy_model

from src.models.spacy import parse_spacy_result


def get_origin_and_destination(sentence: str) -> TripResponse:
    result = spacy_model(sentence)

    result_parsed = parse_spacy_result(result.to_json())

    return find_shortest_trip(result_parsed["departure"], result_parsed["arrival"])
