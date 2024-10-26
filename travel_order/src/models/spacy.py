from fastapi import HTTPException


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
