from enum import Enum

import networkx as nx
from networkx import shortest_path, shortest_path_length

from src.models.trip import TripResponse, TripStep, TripOptionsResponse
from src.config.loader import connections

from src.config.loader import spacy_model
from src.config.loader import G

from src.config.loader import camembert_ner_pipeline
from src.services.camembert_service import parse_camembert_result
from src.services.spacy_service import parse_spacy_result


class AIModels(Enum):
    CAMEMBERT = "CAMEMBERT"
    SPACY = "SPACY"


def find_trip_options(sentence: str, model: AIModels) -> TripOptionsResponse:
    result_parsed = {}
    if model == AIModels.CAMEMBERT:
        result = camembert_ner_pipeline(sentence)

        result_parsed = parse_camembert_result(result)
    if model == AIModels.SPACY:
        result = spacy_model(sentence)

        result_parsed = parse_spacy_result(result.to_json())

    departures = connections[connections['departure_city'].str.lower().str.contains(result_parsed['departure'].lower())][
        ['stop_id_start', 'departure_city']].drop_duplicates()["departure_city"].unique().tolist()

    arrivals = connections[connections['arrival_city'].str.lower().str.contains(result_parsed['arrival'].lower())][
        ['stop_id_end', 'arrival_city']].drop_duplicates()["arrival_city"].unique().tolist()

    return TripOptionsResponse(
        departures=departures,
        arrivals=arrivals
    )


def find_shortest_trip(departure_city: str, arrival_city: str) -> TripResponse | None:
    departure_id = connections[connections['departure_city'] == departure_city]['stop_id_start'].unique()
    arrival_id = connections[connections['arrival_city'] == arrival_city]['stop_id_end'].unique()

    shortest_time = float('inf')
    best_path = None

    for dep_station in departure_id:
        for arr_station in arrival_id:
            try:
                path = shortest_path(G, source=dep_station, target=arr_station, weight='weight')
                time = shortest_path_length(G, source=dep_station, target=arr_station, weight='weight')

                if time < shortest_time:
                    shortest_time = time
                    best_path = path
            except nx.NetworkXNoPath:
                continue

    if best_path:
        detailed_path = get_detailed_path(connections, best_path)
        return TripResponse(
            total_time=shortest_time,
            steps=detailed_path
        )
    return None


def get_detailed_path(connections, path):
    detailed_path = []

    for i in range(len(path) - 1):
        stop_id_start = path[i]
        stop_id_end = path[i + 1]

        step = connections[
            (connections['stop_id_start'] == stop_id_start) &
            (connections['stop_id_end'] == stop_id_end)
            ].iloc[0]

        detailed_path.append(TripStep(
            departure_station=step['departure_station'],
            arrival_station=step['arrival_station'],
            travel_time=step['travel_time'],
            departure_city=step['departure_city'],
            arrival_city=step['arrival_city'],
            stop_lat_start=step['stop_lat_start'],
            stop_lon_start=step['stop_lon_start'],
            stop_lat_end=step['stop_lat_end'],
            stop_lon_end=step['stop_lon_end']
        ))

    return detailed_path
