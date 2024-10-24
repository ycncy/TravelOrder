import os

import spacy
from fastapi import HTTPException

from src.models.trip import TripResponse
from src.services.trip_service import find_shortest_trip

spacy_model = spacy.load(os.path.join(os.path.dirname(__file__), '../../data/spacy/model-best'))


def parse_spacy_result(spacy_json) -> dict:
    sentence_text = spacy_json["text"]

    departure = None
    arrival = None

    for ent in spacy_json["ents"]:
        entity_text = sentence_text[ent["start"]:ent["end"]]
        if ent["label"] == "ORIG":
            departure = entity_text
        elif ent["label"] == "DEST":
            arrival = entity_text

    if not departure or not arrival:
        raise HTTPException(status_code=400, detail="Origin or destination is missing")

    return {
        "sentence": sentence_text,
        "departure": departure,
        "arrival": arrival
    }


def get_origin_and_destination(sentence: str) -> TripResponse:
    result = spacy_model(sentence)

    result_parsed = parse_spacy_result(result.to_json())

    return find_shortest_trip(result_parsed["departure"], result_parsed["arrival"])
