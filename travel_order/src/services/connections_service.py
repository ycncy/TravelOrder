from typing import Tuple

import pandas as pd
import networkx as nx

from src.config.logger import logger


def load_connections_data(data_path: str) -> Tuple[nx.DiGraph, pd.DataFrame]:
    connections = pd.read_csv(data_path)
    logger.info("Loaded SNCF connections")

    G = nx.DiGraph()
    for index, row in connections.iterrows():
        G.add_edge(row['stop_id_start'], row['stop_id_end'], weight=row['travel_time'])

    logger.info(f"Graph created with {len(G.edges)} edges")

    return G, connections
