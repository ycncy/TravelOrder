from fastapi import HTTPException


def parse_camembert_result(camembert_json) -> dict:
    departure = None
    arrival = None

    for ent in camembert_json:
        if ent["entity_group"] == "ORIG":
            departure = ent["word"]
        elif ent["entity_group"] == "DEST":
            arrival = ent["word"]

    if not departure or not arrival:
        raise HTTPException(status_code=400, detail="Origin or destination is missing")

    return {
        "departure": departure,
        "arrival": arrival
    }
