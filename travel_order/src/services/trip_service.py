import os

import networkx as nx
from networkx import shortest_path, shortest_path_length

from src.models.trip import TripResponse, TripStep
from src.services.connections_service import load_connections_data

G, connections = load_connections_data(
    os.path.join(os.path.dirname(__file__), '../../data/output/sncf_connections.csv')
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
